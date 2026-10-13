#!/usr/bin/env python3
"""Step Plan side of the endpoint-parity check (mirror of the Standard probe)."""
import base64, json, os, struct, sys, urllib.error, urllib.request

BASE = "https://api.stepfun.ai/step_plan/v1"
KEY = os.environ.get("STEP_PLAN_API_KEY")
if not KEY:
    sys.exit("STEP_PLAN_API_KEY not set")


def post_json(path, payload, extra=None, timeout=90):
    h = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    h.update(extra or {})
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode(),
                                 method="POST", headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), None
    except urllib.error.HTTPError as e:
        return e.code, e.read(), "http"
    except Exception as e:
        print(f"        transport: {type(e).__name__}: {e}")
        return None, b"", "transport"


def show(name, path, s, raw, err):
    if err == "transport":
        print(f"[{name}] {path} FAILED"); return
    print(f"[{name}] {'OK ' if s == 200 else 'ERR'} HTTP {s}  {path}")
    if s != 200:
        print("        " + raw.decode(errors="replace")[:200].replace("\n", " "))
        return
    try:
        d = json.loads(raw)
    except Exception:
        print(f"        {len(raw)} bytes"); return
    if "choices" in d:
        c = (d["choices"][0].get("message", {}).get("content") or "")[:50]
        print(f"        chat ok: model={d.get('model')} {c!r}")
    elif "output" in d or d.get("object") == "response":
        t = [o.get("content", [{}])[0].get("text", "")[:50]
             for o in d.get("output", []) if o.get("type") == "message"]
        print(f"        responses ok: model={d.get('model')} status={d.get('status')} {t}")
    else:
        print(f"        keys={sorted(d.keys())}")


print("=" * 60)
print("Step Plan side of endpoint parity")
print(f"base: {BASE}")
print("=" * 60)

s, raw, err = post_json("/chat/completions", {
    "model": "step-3.5-flash-2603",
    "messages": [{"role": "user", "content": "say hi"}], "max_tokens": 4})
show("chat", "/chat/completions", s, raw, err)

s, raw, err = post_json("/responses", {
    "model": "step-5-preview", "input": "say hi", "max_output_tokens": 512})
show("responses", "/responses", s, raw, err)

wav = (b"RIFF" + struct.pack("<I", 36 + 32000) + b"WAVEfmt "
       + struct.pack("<IHHIIHH", 16, 1, 1, 16000, 32000, 2, 16)
       + b"data" + struct.pack("<I", 32000) + b"\x00" * 32000)
s, raw, err = post_json("/audio/asr/sse", {"audio": {
    "data": base64.b64encode(wav).decode(),
    "input": {"transcription": {"model": "stepaudio-2.5-asr", "language": "en"},
              "format": {"type": "wav", "rate": 16000, "bits": 16, "channel": 1}}}},
    extra={"Accept": "text/event-stream"})
if err != "transport":
    print(f"[asr] {'OK ' if s == 200 else 'ERR'} HTTP {s}  /audio/asr/sse")
    print("        " + raw.decode(errors="replace")[:150].replace("\n", " "))

s, raw, err = post_json("/audio/speech", {
    "model": "stepaudio-2.5-tts", "input": "hi", "voice": "vibrant-youth"})
show("tts", "/audio/speech", s, raw, err)
if s == 200:
    print(f"        audio bytes: {len(raw)}")

# messages (Anthropic wire format) — the one endpoint not probed on Standard
s, raw, err = post_json("/messages", {
    "model": "step-3.5-flash", "max_tokens": 8,
    "messages": [{"role": "user", "content": "say hi"}]},
    extra={"anthropic-version": "2023-06-01"})
show("messages", "/messages", s, raw, err)

# files — multipart .wav
boundary = "----planprobe4b"
body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"purpose\""
        f"\r\n\r\nstorage\r\n--{boundary}\r\nContent-Disposition: form-data;"
        f" name=\"file\"; filename=\"probe.wav\"\r\nContent-Type: audio/wav"
        f"\r\n\r\n").encode() + wav + f"\r\n--{boundary}--\r\n".encode()
req = urllib.request.Request(BASE + "/files", data=body, method="POST",
    headers={"Authorization": f"Bearer {KEY}",
             "Content-Type": f"multipart/form-data; boundary={boundary}"})
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        print(f"[files] OK  HTTP {r.status}  /files  {r.read().decode()[:150]}")
except urllib.error.HTTPError as e:
    print(f"[files] ERR HTTP {e.code}  /files  "
          f"{e.read().decode(errors='replace')[:150]}")
except Exception as e:
    print(f"[files] transport {type(e).__name__}: {e}")

print("=" * 60)
print("done")
