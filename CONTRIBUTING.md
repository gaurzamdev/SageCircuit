# Contributing to SageCircuit

We appreciate contributions to SageCircuit, a local, from-scratch AI project. Changes
are assessed for correctness, repeatability, and alignment with the project's
security constraints.

## Start here

- Read [README.md](README.md), [MODEL_CARD.md](MODEL_CARD.md), and
  [SECURITY.md](SECURITY.md).
- When reporting a defect, provide the release, OS, Python and numpy versions,
  the command you ran, and a minimal way to reproduce it.
- Feature proposals should describe the user need and fit with local-first
  operation. Discuss larger proposals in an issue before implementation.

## Prepare a development checkout

```bash
git clone https://github.com/gaurzamdev/SageCircuit.git
cd SageCircuit
python -m pip install -r requirements.txt
python scripts/prepare_assets.py
python -m unittest discover -s source/tests -v
```

Setup generates the expanded database, which Git ignores. Do not add that
file to a commit; `assets/tensei.db.gz` is the release snapshot.

## Change guidelines

- Limit each change to its intended purpose; avoid unrelated formatting edits.
- Keep current behavior unless changing it is part of the proposal.
- Include tests or revise existing tests when behavior changes.
- Preserve local-first execution and the no-pretrained-model requirement.
- Do not add telemetry, analytics, undisclosed network requests, or a
  mandatory hosted service.
- Keep generated outputs, model files, logs, caches, benchmark results, and
  signing credentials out of commits.
- Explain the need for any new dependency, then update requirements and docs.

## Style and implementation

- Python 3.12+; prefer the standard library unless a dependency is justified.
- Give functions clear responsibilities and use descriptive names.
- Use comments to explain reasoning that is not evident from the implementation.
- Save source and documentation as UTF-8.
- Keep the web UI free of dependencies unless a concrete need justifies one.
- Before opening a pull request, run `python -m compileall -q source`.

## Tests and performance checks

```bash
python -m unittest discover -s source/tests -v
cd source
TENSEI_OFFLINE=1 TENSEI_NO_LEARN=1 python bench/bench100.py
```

Do not specialize implementation for individual benchmark prompts. If a
change affects benchmark scores, explain the broader behavior responsible.

## Updating the knowledge snapshot or model

When retraining the model or revising its packaged knowledge:

1. Rebuild the snapshot intentionally.
2. Regenerate `assets/tensei.db.gz`.
3. Update `assets/SHA256SUMS` and `assets/README.md`.
4. Update `MODEL_CARD.md` and `CHANGELOG.md`.
5. Run the full build and benchmark.
6. Do not commit the uncompressed database or built `.tsei`/`.pyz`.

Asset preparation validates both the snapshot digest and its record totals.
Update those checks together with any intentional database revision.

## Android-specific work

- No keystore or signing password may be committed.
- Keep the model out of Git; document how to stage it.
- Test both Termux and the Chaquopy project when the change affects mobile.
- Keep Android permissions minimal.

## Opening a pull request

A useful pull request explains:

- what changed and why,
- the commands used to test,
- benchmark impact if relevant,
- any security or privacy implications,
- documentation updates.

Contributions are provided under the project's MIT license.
