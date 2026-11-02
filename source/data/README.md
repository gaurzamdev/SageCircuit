# Database directory

Prepare this directory before building or running from source:

```bash
python scripts/prepare_assets.py
```

The preparation script checks `assets/tensei.db.gz` and expands it here as
`tensei.db`. The expanded database is not tracked because it exceeds GitHub's
individual-file size limit.

During normal operation, learned records are saved under the active
`TENSEI_HOME` (typically `~/.tensei_ai/data/tensei.db`), rather than in this
source snapshot.
