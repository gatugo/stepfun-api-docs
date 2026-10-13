#!/usr/bin/env python3
"""ASR + files shape variants — find the accepted request layout."""
import base64, json, os, struct, sys, urllib.error, urllib.request

BASE = "https://api.stepfun.ai/v1"
KEY = os.environ["STEP_PLAN_API_KEY"]

wav = (b"RIFF" + struct.pack("<I", 36 + 32000) + b"WAVEfmt "
       + struct.pack("<IHHIIHH", 16, 1, 1, 16000, 32000, 2, 16)
       + b"data" + struct.pack("<I", 32000) + b"\x00" * 32000)
b64 = base64.b64encode(wav).decode()

def try_json(label, payload, path="/audio/asr/sse", headers=None):
    h = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
         "Accept": "text/event-stream"}
    h.update(headers or {})
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode(),
                                 method="POST", headers=h)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode(errors="replace")
            print(f"[{label}] OK {r.status} :: {body[:160]!r}")
    except urllib.error.HTTPError as e:
        print(f"[{label}] {e.code} :: {e.read().decode(errors='replace')[:160]}")
    except Exception as e:
        print(f"[{label}] transport {type(e).__name__}: {e}")

print("--- ASR variants ---")
# A: docs shape (input.format)
try_json("A input.format.wav", {"audio": {"data": b64, "input": {
    "transcription": {"model": "stepaudio-2.5-asr", "language": "en"},
    "format": {"type": "wav", "rate": 16000, "bits": 16, "channel": 1}}}})
# B: format at audio level
try_json("B audio.format.wav", {"audio": {"data": b64,
    "format": {"type": "wav", "rate": 16000, "bits": 16, "channel": 1},
    "input": {"transcription": {"model": "stepaudio-2.5-asr"}}}})
# C: pcm, docs example verbatim
pcm = b"\x00" * 32000
try_json("C input.format.pcm", {"audio": {"data": base64.b64encode(pcm).decode(),
    "input": {"transcription": {"model": "stepaudio-2.5-asr", "language": "zh"},
              "format": {"type": "pcm", "codec": "pcm_s16le",
                         "rate": 16000, "bits": 16, "channel": 1}}}})
# D: minimal — only data
try_json("D data-only", {"audio": {"data": b64}})
# E: format as a plain string
try_json("E format-string", {"audio": {"data": b64, "format": "wav"}})
# F: audio_format at top level
try_json("F audio_format", {"audio": {"data": b64}, "audio_format": "wav",
                            "model": "stepaudio-2.5-asr"})

print("--- Files variants ---")
def try_file(label, filename, data, ctype):
    boundary = "----probe7c1"
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"purpose\""
            f"\r\n\r\nstorage\r\n--{boundary}\r\nContent-Disposition: form-data;"
            f" name=\"file\"; filename=\"{filename}\"\r\nContent-Type: {ctype}"
            f"\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(BASE + "/files", data=body, method="POST",
        headers={"Authorization": f"Bearer {KEY}",
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            print(f"[{label}] OK {r.status} :: {r.read().decode()[:200]}")
    except urllib.error.HTTPError as e:
        print(f"[{label}] {e.code} :: {e.read().decode(errors='replace')[:200]}")
    except Exception as e:
        print(f"[{label}] transport {type(e).__name__}: {e}")

try_file("files .wav", "probe.wav", wav, "audio/wav")
try_file("files .mp3", "probe.mp3", b"\xff\xfb\x90\x00" + b"\x00" * 200, "audio/mpeg")
try_file("files .png", "probe.png",
         base64.b64decode(
             "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8"
             "DwHwAFAAH/q842iQAAAABJRU5ErkJggg=="), "image/png")
