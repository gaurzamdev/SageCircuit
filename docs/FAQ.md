# SageCircuit: common questions

## Does SageCircuit depend on Llama or GGUF?

No. The project does not load Llama checkpoints or GGUF files, and it does not
rely on Ollama, llama.cpp, or a hosted language model. Its language component
is trained from scratch with numpy and saved in the project's TSM1/TSMC
container. A `.tsei` file is not a GGUF file with a different extension.

## Is a GPU required?

No. CPU execution is supported. Installing numpy is recommended; the optional
C sampling helper can be omitted.

## What needs to be installed?

Install Python 3.12 or later and numpy. The `.pyz` release contains neither
CPython nor numpy. On Termux, install both with
`pkg install -y python python-numpy`.

## How do the `.pyz` and `.tsei` files differ?

`TenSeiAi.pyz` packages the application runtime, command-line tools, web
interface, and an embedded model. `TenSeiAi.tsei` is a portable model
container; it cannot run by itself. Use it with the `.pyz` runtime or load it
through an application.

```bash
python TenSeiAi.pyz TenSeiAi.tsei
```

## Can I use it without internet access?

The engine runs locally, and the HTTP server listens on localhost by default.
Web research is optional. To disable online research for a session:

```bash
TENSEI_OFFLINE=1 python TenSeiAi.pyz
```

On Windows PowerShell:

```powershell
$env:TENSEI_OFFLINE = "1"
py TenSeiAi.pyz
```

## Is telemetry collected?

No analytics or telemetry are built in. When web research is enabled, search
terms and visited URLs are sent to external services. Set
`TENSEI_OFFLINE=1` to disable those requests.

## Why is the model compact?

The approximately 19.7-million-parameter language core fits a CPU-focused
runtime and portable package. Retrieval, grounding, deterministic solvers, and
the curated database support the wider system. It is not a frontier-scale
model; see the model card for its limitations.

## How should I interpret the benchmark?

The hybrid system passed all 100 checks in the fixed v8 evaluation. This score
describes that specific test set, not general capability. Read
[BENCHMARK.md](../BENCHMARK.md) before quoting the result.

## Where is learned data kept?

Runtime learning is stored locally in SQLite under `TENSEI_HOME` (normally
`~/.tensei_ai`) and is not uploaded. Remove that directory to reset runtime
state. Builds and benchmarks use a temporary or source database.

## May I use SageCircuit commercially?

The code and weights use the MIT license; read [LICENSE](../LICENSE). Users
are responsible for generated content and for rights to material they add.

## How do I update the installation?

Download the latest `TenSeiAi.pyz` release and, if needed, `TenSeiAi.tsei`,
or rebuild the artifacts from source. Existing runtime data stays in
`TENSEI_HOME` unless you delete it.

## Why is the knowledge snapshot compressed?

The expanded SQLite file is 102.5 MiB, larger than GitHub's 100 MB file cap.
The repository instead contains a 47.4 MiB gzip archive, which
`scripts/prepare_assets.py` expands. Git LFS is not needed.

## Can I integrate it with another application?

Yes. Use the local HTTP interface, or call `tensei.android.start` and
`tensei.android.ask` from an Android app through Chaquopy. See
[API.md](API.md) and [ANDROID.md](ANDROID.md).

## Why is the initial launch slower?

The first launch extracts and loads the model into `~/.tensei_ai`. Later
launches reuse that copy. A temporary home directory is cleared between runs,
so extraction will happen again.

## How can I reset local state?

Delete the runtime directory:

```bash
rm -rf ~/.tensei_ai
```

On Windows:

```powershell
Remove-Item -Recurse -Force "$HOME\.tensei_ai"
```

This removes learned rows and the installed model copy without changing the
release artifact or source snapshot.
