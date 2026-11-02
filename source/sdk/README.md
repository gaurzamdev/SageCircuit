# SDK clients for SageCircuit

SageCircuit exposes a localhost HTTP service at `http://127.0.0.1:8765`. Programs
written in any language can send JSON requests to it. To extract the sample
clients from the standalone application, run:

```bash
python TenSeiAi.pyz sdk --out tensei_sdk
```

Start the engine first:

```bash
python TenSeiAi.pyz serve --port 8765
```

## Routes used by the clients

| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/api/ask` | `{"q": "...", "wait": true}` | direct answer |
| POST | `/api/ask` | `{"q": "..."}` | `{"id": "..."}` job id |
| GET | `/api/job?id=...` | none | job status and result |
| POST | `/v1/chat/completions` | OpenAI format | OpenAI-compatible response |
| GET | `/api/stats` | none | live brain and memory stats |

## Check the chat endpoint

```bash
curl -s http://127.0.0.1:8765/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"tensei-1","messages":[{"role":"user","content":"hello"}]}'
```

## Client examples in this directory

- `python/tensei_client.py` standard-library Python client
- `java/TenSeiClient.java` Java 11+ client using `java.net.http`
- `kotlin/TenSeiAndroid.kt` Kotlin/Android `HttpURLConnection` helper
- `rust/tensei_client.rs` Rust client using only the standard library
- `cpp/tensei_client.cpp` C++17 POSIX client with no dependencies

These files are reference implementations rather than released packages.
Review them and adapt them to your application. The server is designed for
local use and does not provide authentication. See
[`docs/API.md`](../../docs/API.md) and [`SECURITY.md`](../../SECURITY.md).
