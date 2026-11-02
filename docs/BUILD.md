# Building and publishing releases

## Prerequisites

- Python version 3.12 or later.
- numpy 2.x.
- Optional C compiler (`cc`, `gcc`, or `clang`) to compile the `cspeed`
  sampler; the application also works without this helper.
- Approximately 1 GB of available disk space for the archive, expanded
  database, and build outputs.

```bash
python -m pip install -r requirements.txt
```

## 1. Prepare the local knowledge database

```bash
python scripts/prepare_assets.py
```

This command performs the following checks and actions:

1. Verifies `assets/tensei.db.gz` against `assets/SHA256SUMS`.
2. Decompresses it to `source/data/tensei.db`.
3. Verifies the SQLite integrity check and the expected row counts.
4. Leaves an existing `source/data/tensei.db` in place if it differs from the
   packaged snapshot.

To deliberately overwrite a locally modified database with the packaged copy:

```bash
python scripts/prepare_assets.py --force
```

Git ignores the expanded database file.

## 2. Check the test suite

```bash
python -m unittest discover -s source/tests -v
```

Tests run offline with a temporary `TENSEI_HOME`, keeping your personal
runtime database separate.

## 3. Create the release files

```bash
python scripts/build_release.py
```

Build inputs are copied into a temporary workspace (`data/`, `brains/`,
`web/`, and `sdk/`), so the source database is not changed.

Outputs:

```text
dist/TenSeiAi.tsei
dist/TenSeiAi.pyz
dist/SHA256SUMS
```

The script requires numpy, prepares the database when necessary, disables
network access and learning for the build, validates both file headers, and
generates SHA-256 checksums.

### Build options

```bash
python scripts/build_release.py --out-dir build/release
python scripts/build_release.py --no-prepare
python scripts/build_release.py --prepare-force
```

Use `--no-prepare` after restoring and checking the database yourself.
`--prepare-force` replaces a changed source database with the packaged
snapshot.

## 4. Verify the artifacts

```bash
python dist/TenSeiAi.pyz ask "What is a black hole?"
python dist/TenSeiAi.pyz inspect dist/TenSeiAi.tsei
python dist/TenSeiAi.pyz dist/TenSeiAi.tsei
python dist/TenSeiAi.pyz serve --port 8765
```

The `.tsei` output stores the model; it is not an executable by itself. Launch
it with the `.pyz` runtime or install it from an application using
`tensei.model_file.install_model`.

## Automated builds with GitHub Actions

The `.github/workflows/build.yml` workflow starts for:

- manual dispatch,
- pushes to `main`,
- version tags matching `v*`,
- pull requests targeting `main`.

Each run checks out the project, installs its pinned numpy version, restores
the knowledge asset, runs tests, builds the two outputs, checks their headers,
and uploads the release files. When triggered by a tag, it also publishes a
GitHub Release containing the files and checksums.

Recommended first release:

```bash
git tag v8.0.0
git push origin v8.0.0
```

The workflow needs neither a signing key nor a model download. It uses
`GITHUB_TOKEN` with permissions scoped to each job.

## Keeping large files out of Git

Because GitHub limits individual files to 100 MB, the 102.51 MiB
(107,487,232-byte) database is checked in as a 47.43 MiB gzip archive:

```text
assets/tensei.db.gz   49,733,956 bytes
```

This archive fits under the limit without Git LFS. Local setup and CI recreate
the expanded database. Its expected digest is recorded in
`assets/SHA256SUMS`.

Keep these generated or private files out of commits:

- `dist/`
- `*.pyz` or `*.tsei`
- `source/data/tensei.db`
- runtime databases under `~/.tensei_ai`
- Android keystores
- logs, benchmark result dumps, or caches

## Building for Android

Follow [ANDROID.md](ANDROID.md). Provide Android signing credentials through a
secure local environment; never add them to the repository.

## Common build problems

### `ModuleNotFoundError: numpy`

```bash
python -m pip install -r requirements.txt
```

Install the dependency into the Python interpreter used to launch
`TenSeiAi.pyz`.

### Database checksum mismatch

Check the digest in `assets/SHA256SUMS`, or fetch a fresh copy of the
repository. An incomplete checkout may contain a damaged archive.

### Existing database mismatch

The database in your source tree does not match the shipped snapshot. Move it
aside or explicitly restore the packaged copy:

```bash
python scripts/prepare_assets.py --force
```

### The build is slow

The `.tsei` pack uses LZMA for the database and model components, so an initial
build may take several minutes. Later runs can reuse the restored database.
