# Benchmark method and results

This fixed, intentionally limited test is designed to make runs comparable.
It checks the complete SageCircuit pipeline against a repeatable set of prompts;
it does not measure broad, general-purpose capability.

## Test configuration

| Property | Value |
|---|---|
| Questions | 100, five domains, 20 each |
| Mode | Offline (`TENSEI_OFFLINE=1`), no runtime learning (`TENSEI_NO_LEARN=1`) |
| Database | Temporary copy of the shipped snapshot |
| Machine | Development laptop; CPU only |
| Harness | `source/bench/bench100.py` |

The benchmark runner ships with the repository and does not consult a
benchmark-only answer key. It sends questions through the same routing,
retrieval, solver, and response-composition stages as normal use.

## Measured outcome

| Check | Result |
|---|---:|
| Correct checks | **100/100** |
| Warm run | **5.0 s** total |
| Average warm latency | **0.05 s/question** |

Results depend on the machine, filesystem cache, and temporary runtime
directory. Mobile-device timing may be different.

## Reading the result

SageCircuit combines several techniques. Its factual performance on this set
relies substantially on curated records, constrained retrieval, and
deterministic solvers rather than unconstrained text generation by the
19.7-million-parameter core. This is the intended tradeoff for a small local
package.

The language core is not strong at free-form writing. Shipped metadata reports
5.43% held-out next-token accuracy. The combined system performs better on
this test because it can retrieve supporting material or use a solver when
appropriate.

Do not present `100/100` as proof of parity with a frontier model. Attribute
the number to this particular benchmark, procedure, and build.

## Run the evaluation again

```bash
python scripts/prepare_assets.py
cd source
TENSEI_OFFLINE=1 TENSEI_NO_LEARN=1 python bench/bench100.py
```

Windows PowerShell:

```powershell
python scripts\prepare_assets.py
Set-Location source
$env:TENSEI_OFFLINE = "1"
$env:TENSEI_NO_LEARN = "1"
python bench\bench100.py
```

The runner copies the database and trained weights into a temporary home,
leaving the source snapshot unchanged. It writes generated results to
`bench/bench100_results.json` beside the runner; this output is not checked in.

## Check release-file integrity

GitHub Actions builds each release and publishes a
`dist/SHA256SUMS`. To verify a downloaded artifact:

```bash
grep 'TenSeiAi.pyz$' SHA256SUMS | sha256sum -c -
```

Windows PowerShell:

```powershell
$expected = (Get-Content SHA256SUMS | Where-Object { $_ -match 'TenSeiAi.pyz$' }).Split()[0]
$actual = (Get-FileHash TenSeiAi.pyz -Algorithm SHA256).Hash.ToLower()
if ($actual -ne $expected) { throw "Checksum mismatch" } else { "Checksum OK" }
```
