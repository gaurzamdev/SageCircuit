# Knowledge snapshot asset

The `tensei.db.gz` archive contains the project's initial knowledge database.

| Property | Value |
|---|---:|
| Format | gzip-compressed SQLite 3 database |
| Uncompressed size | 107,487,232 bytes (102.51 MiB) |
| Compressed size | 49,733,956 bytes (47.43 MiB) |
| SHA-256 of compressed file | see `SHA256SUMS` |
| Q&A rows | 19,895 |
| Passages | 7,460 |
| Topics | 400 |

## Reason for storing a compressed copy

GitHub's per-file limit is 100 MB, while the expanded SQLite database is
slightly larger. This repository therefore keeps a deterministic gzip copy.
Before a local run or build, `scripts/prepare_assets.py` checks its digest and
recreates `source/data/tensei.db`.

This archive is a project asset, not the database used for an individual's
runtime activity. Runtime learning goes to the active `TENSEI_HOME`, normally
`~/.tensei_ai`.

```bash
python scripts/prepare_assets.py
python scripts/prepare_assets.py --force
```
