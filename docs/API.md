# HTTP API for local applications

The web chat and HTTP endpoints run in the same SageCircuit process. By default,
the server is available at `http://127.0.0.1:8765`. This interface is intended
for software on the local machine, not a public, multi-user deployment.

Start it with:

```bash
python TenSeiAi.pyz serve --port 8765
```

## Available routes

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/` | Local web chat |
| `GET` | `/api/stats` | Memory, brain, and uptime statistics |
| `POST` | `/api/ask` | Ask a question |
| `GET` | `/api/job?id=...` | Poll an asynchronous job |
| `GET` | `/api/feed?since=0` | Recent learning/training events |
| `GET` | `/api/topics` | Current topic queue |
| `POST` | `/api/feedback` | Rate a stored answer |
| `POST` | `/api/autofeed` | Start or stop optional background research |
| `POST` | `/api/train` | Start a background brain training run |
| `GET` | `/v1/models` | OpenAI-style model list |
| `POST` | `/v1/chat/completions` | OpenAI-compatible chat completion |

## Request format and size

POST requests must contain valid JSON with an object at the top level. Bodies
are limited to 1 MiB. Question prompts and the `content` of a user message
must be strings. Invalid JSON or field types receive a `400` response; a body
over the limit receives `413`. Error responses include an `error` field with
the reason.

## Submit a question

Wait for an answer in the same request:

```bash
curl -s http://127.0.0.1:8765/api/ask \
  -H 'Content-Type: application/json' \
  -d '{"q":"What is a black hole?","wait":true}'
```

The response contains `answer`, `steps`, `sources`, `mode`, `confidence`, and
`took_s`.

For a background job, omit `wait`:

```bash
curl -s http://127.0.0.1:8765/api/ask \
  -H 'Content-Type: application/json' \
  -d '{"q":"Explain binary search"}'
```

```json
{"id":"a1b2c3d4e5f6"}
```

Use the returned job ID to check progress and retrieve the result:

```bash
curl -s "http://127.0.0.1:8765/api/job?id=a1b2c3d4e5f6"
```

## OpenAI-shaped chat completion

```bash
curl -s http://127.0.0.1:8765/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "tensei-1",
    "messages": [
      {"role": "user", "content": "Write a Python function to reverse a string"}
    ]
  }'
```

Responses use the familiar `choices[0].message.content` structure. SageCircuit
uses the most recent user message as the prompt; the supplied model name is
informational.

## Read runtime statistics

```bash
curl -s http://127.0.0.1:8765/api/stats
```

The result includes memory totals, model metadata, background-feed status,
and server uptime.

## Record answer feedback

```bash
curl -s http://127.0.0.1:8765/api/feedback \
  -H 'Content-Type: application/json' \
  -d '{"qa_id":123,"rating":1}'
```

Provide an integer `rating`: positive values indicate a helpful response and
negative values indicate an unhelpful one. The precise handling is documented
by `Memory.set_feedback`.

## Start or stop optional web research

Background autofeed starts disabled. Enable or disable it with an explicit
action:

```bash
curl -s http://127.0.0.1:8765/api/autofeed \
  -H 'Content-Type: application/json' \
  -d '{"action":"start"}'

curl -s http://127.0.0.1:8765/api/autofeed \
  -H 'Content-Type: application/json' \
  -d '{"action":"stop"}'
```

When active, the process can search online, save passages, and later retrain.
Set `TENSEI_OFFLINE=1` to keep it from accessing the network.

## Deployment safety

- The server does not authenticate callers.
- Cross-origin access is permissive for development use.
- By default, it listens on `127.0.0.1`.
- Avoid binding it to `0.0.0.0` on a network you do not trust.
- For access from other machines, use a reverse proxy that provides TLS,
  authentication, request throttling, and logging.

Review [SECURITY.md](../SECURITY.md) before making it remotely accessible.
