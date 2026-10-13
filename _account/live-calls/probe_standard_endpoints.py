#!/usr/bin/env python3
"""Q-STD-03 — Standard-channel endpoint parity probe.

One cheap live call per endpoint against https://api.stepfun.ai/v1.
Key comes from $STEP_PLAN_API_KEY (never echoed).
Shapes follow bundle/by-task/{chat-apis,audio,files}.md.
"""
import base64
import json
import os
import struct
import sys
import urllib.error
import urllib.request

BASE = "https://api.stepfun.ai/v1"
KEY = os.environ.get("STEP_PLAN_API_KEY")
if not KEY:
    sys.exit("STEP_PLAN_API_KEY not set")


def post_json(path, payload, extra_headers=None, timeout=90):
    body = json.dumps(payload).encode()
    headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    headers.update(extra_headers or {})
    req = urllib.request.Request(BASE + path, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), None
    except urllib.error.HTTPError as e:
        return e.code, e.read(), "http"
    except Exception as e:
        print(f"        transport error: {type(e).__name__}: {e}")
        return None, b"", "transport"


def post_multipart(path, fields, files, timeout=90):
    boundary = "----stepfunprobe9f3a"
    parts = []
    for name, value in fields:
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\""
            f"\r\n\r\n{value}\r\n".encode())
    for name, filename, ctype, data in files:
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; "
            f"filename=\"{filename}\"\r\nContent-Type: {ctype}\r\n\r\n".encode()
            + data + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        BASE + path, data=b"".join(parts), method="POST",
        headers={"Authorization": f"Bearer {KEY}",
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), None
    except urllib.error.HTTPError as e:
        return e.code, e.read(), "http"
    except Exception as e:
        print(f"        transport error: {type(e).__name__}: {e}")
        return None, b"", "transport"


def report(name, path, status, raw, err):
    if err == "transport":
        print(f"[{name}] {path}  FAILED")
        return
    label = "OK " if status == 200 else "ERR"
    print(f"[{name}] {label} HTTP {status}  {path}")
    if status != 200:
        try:
            print("        " + raw.decode(errors="replace")[:250].replace("\n", " "))
        except Exception:
            pass
        return
    try:
        d = json.loads(raw)
    except Exception:
        print(f"        non-JSON body, {len(raw)} bytes")
        return
    if "choices" in d:
        content = (d["choices"][0].get("message", {}).get("content") or "")[:60]
        print(f"        chat ok: model={d.get('model')} content={content!r}")
    elif "output" in d or d.get("object") == "response":
        texts = [o.get("content", [{}])[0].get("text", "")[:60]
                 for o in d.get("output", []) if o.get("type") == "message"]
        print(f"        responses ok: model={d.get('model')} status={d.get('status')} "
              f"text={texts}")
    else:
        print(f"        keys={sorted(d.keys())}")


print("=" * 64)
print("Q-STD-03 — Standard channel endpoint parity")
print(f"base: {BASE}   key: {'<set>' if KEY else '<missing>'}")
print("=" * 64)

# --- 1. Chat Completions (control: known-good) --------------------------
s, raw, err = post_json("/chat/completions", {
    "model": "step-3.5-flash-2603",
    "messages": [{"role": "user", "content": "say hi"}],
    "max_tokens": 4,
})
report("chat", "/chat/completions", s, raw, err)

# --- 2. Responses API — step-5-preview (corpus says only 5-preview/3.7-flash)
s, raw, err = post_json("/responses", {
    "model": "step-5-preview", "input": "say hi", "max_output_tokens": 512,
})
report("responses/step-5-preview", "/responses", s, raw, err)

s, raw, err = post_json("/responses", {
    "model": "step-3.7-flash", "input": "say hi", "max_output_tokens": 512,
})
report("responses/step-3.7-flash", "/responses", s, raw, err)

# --- 3. ASR one-shot SSE — nested audio.* shape --------------------------
wav = (b"RIFF" + struct.pack("<I", 36 + 32000) + b"WAVEfmt "
       + struct.pack("<IHHIIHH", 16, 1, 1, 16000, 32000, 2, 16)
       + b"data" + struct.pack("<I", 32000) + b"\x00" * 32000)
s, raw, err = post_json("/audio/asr/sse", {
    "audio": {
        "data": base64.b64encode(wav).decode(),
        "input": {
            "transcription": {"model": "stepaudio-2.5-asr", "language": "en"},
            "format": {"type": "wav", "rate": 16000, "bits": 16, "channel": 1},
        },
    },
}, extra_headers={"Accept": "text/event-stream"})
if err != "transport":
    print(f"[asr] {'OK ' if s == 200 else 'ERR'} HTTP {s}  /audio/asr/sse")
    print("        " + raw.decode(errors="replace")[:250].replace("\n", " "))

# --- 4. TTS one-shot — system voice id ----------------------------------
s, raw, err = post_json("/audio/speech", {
    "model": "stepaudio-2.5-tts", "input": "hi", "voice": "vibrant-youth",
})
report("tts", "/audio/speech", s, raw, err)
if s == 200:
    print(f"        audio bytes: {len(raw)}")

# --- 5. Files — multipart upload, purpose=storage ------------------------
s, raw, err = post_multipart(
    "/files", [("purpose", "storage")],
    [("file", "probe.txt", "text/plain", b"hello stepfun parity probe\n")])
report("files(multipart)", "/files", s, raw, err)

# --- 6. Files list ------------------------------------------------------
req = urllib.request.Request(BASE + "/files", method="GET",
                             headers={"Authorization": f"Bearer {KEY}"})
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read())
        print(f"[files-list] OK  HTTP {r.status}  /files  ({len(d.get('data', []))} files)")
except urllib.error.HTTPError as e:
    print(f"[files-list] ERR HTTP {e.code}  /files  {e.read()[:150].decode(errors='replace')}")

print("=" * 64)
print("done")
