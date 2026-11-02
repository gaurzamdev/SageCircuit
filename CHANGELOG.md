# SageCircuit release history

This log records the notable updates to the application and its release
packages. Versions follow the project's semantic-versioning scheme.

Earlier release artifacts retain their original TenSeiAi filenames.

## 8.1.0 - 2026-10-20

### Added

- **Standalone text-generation improvements**:
  - Added repetition and recency controls to reduce loops and repeated n-gram
    patterns.
  - Added strict 3-gram blocking to avoid recursive phrase repetition.
  - Added nucleus sampling (`top-p = 0.88`, `top-k = 35`) and a configurable
    temperature.
  - Preserved prompt anchors so the topic remains available beyond the
    8-token attention window.
  - Added topic-aware passage selection and automatic grounding in semantic
    memory.
  - Added output cleanup for casing, acronyms, and punctuation.
  - Implemented the n-gram transition builder and refresh operations
    (`build_ngrams` / `rebuild_ngrams`).

### Changed

- Corrected `TransMoE.load()` so the vocabulary's `unk`, `bos`, `eos`, and
  `pad` IDs are initialized.
- Updated `Thinker._generate_reply()` to ground language-model output in
  retrieved semantic-memory passages.
- Changed the model-container LZMA preset to 6 for faster on-device export.

## 8.0.0 - 2026-10-20

### Added

- Established a public repository layout with a compressed knowledge
  snapshot.
- Added a GitHub Actions workflow to build `TenSeiAi.pyz`, `TenSeiAi.tsei`,
  and their checksum file.
- Enabled release publication from version tags.
- Added CodeQL, Dependabot, issue templates, and a security policy.
- Added guides for building, system design, the API, Android, model details,
  evaluation, and common questions.
- Added SHA-256 verification for the database archive and release outputs.

### Changed

- Set the release version to 8.0.0.
- Removed third-party font loading from the web interface.
- Made Android signing depend on the user's environment; no keystore is
  distributed.
- Switched source setup to restore the SQLite database from
  `assets/tensei.db.gz` rather than track its expanded form.

### Removed

- Removed old model packages and backups.
- Removed database copies and generated benchmark output.
- Removed logs, caches, temporary utilities, and downloaded datasets.
- Removed embedded Android signing credentials.

### Verification

- Confirmed 19,895 question-and-answer rows, 7,460 passages, and 400 topics.
- Passed SQLite's integrity check.
- Passed the 100-question offline evaluation.
- Built both release artifacts from a clean source checkout.
