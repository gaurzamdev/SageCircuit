# SageCircuit: model and system notes

## At a glance

| Field | Value |
|---|---|
| Name | SageCircuit |
| Release | 8.0.0 |
| Model type | Hybrid retrieval + deterministic solvers + from-scratch Transformer/MoE language core |
| Language core | 2-block Transformer with top-1 Mixture-of-Experts feed-forward layers |
| Parameters | 19,740,464 |
| Dimensions | dim 512, 2 blocks, 2 heads, 4 experts, FFN 1024, vocab 9000 |
| Training | 7,456 samples, 1,202 seconds, hand-written numpy backpropagation |
| Final training loss | 7.9136 |
| Perplexity | 2734.08 |
| Held-out next-token accuracy | 5.43% |
| Knowledge snapshot | 19,895 Q&A rows, 7,460 passages, 400 topics |
| Container | TSM1/TSMC, LZMA-compressed |
| Runtime | Python 3.12+ and numpy; CPU only |
| License | MIT |

SageCircuit's language component is a trained model, intentionally constrained in size.
Measured system quality also depends on retrieval, grounding checks,
deterministic solvers, and response composition. The language component alone
is not a frontier-scale chat model.

## Container contents

`TenSeiAi.tsei` contains:

- `brains/` trained numpy arrays: intent classifier, relevance scorer,
  embedding projection, LM vocabulary, and Transformer/MoE weights.
- `data/tensei.db` the SQLite knowledge and runtime database snapshot.
- `web/index.html` the local chat UI.

`TenSeiAi.pyz` carries the same TSM1 model along with the application entry
point and packaged engine modules. Python and numpy must still be available
from the host.

## Suitable uses

- Ask local questions using the included knowledge snapshot.
- Experiment privately with a small language system, including offline.
- Explore the interaction of retrieval, routing, and a compact Transformer.
- Integrate SageCircuit into a local web, desktop, or Android application.
- Study a reproducible model-container design that does not use GGUF.

## Uses this project is not designed for

- Decisions with serious medical, legal, financial, or safety consequences.
- Representing SageCircuit as a frontier-level general-purpose language model.
- Public, unattended operation without access controls and request limits.
- Treating generated output as a replacement for expert review.
- Creating or sharing unlawful material.

## Training process and data sources

The language component was trained from scratch using prepared text samples
and limited CPU resources. The knowledge snapshot contains curated question
and answer records, reference passages, code samples, and general-knowledge
material. Private user conversations are not part of the repository; runtime
learning remains under the user's `TENSEI_HOME`.

Training utilities and seed scripts are located in `source/tools/` and
`source/tensei/`. The benchmark runner is `source/bench/bench100.py`.

## Evaluation results

The v8 offline benchmark is a fixed 100-question set across five domains:

| Metric | Result |
|---|---:|
| Answer checks passed | 100/100 |
| Warm run time | 5.0 s total (about 0.05 s/question) |

These figures come from a fixed evaluation, not a general capability rating.
The prompts align with the system's retrieval, solver, and knowledge coverage.
See [BENCHMARK.md](BENCHMARK.md) for the full procedure and qualifications.

## Important limitations

- Free-form writing quality is limited compared with current large models.
- Responses may be repetitive, incomplete, or based on a misread prompt.
- Retrieved passages may be inaccurate or no longer current.
- The packaged knowledge is limited in scope and does not update as an
  encyclopedia would.
- Online research depends on network availability and source quality.
- Harmful-content checks provide only basic coverage.
- Code output is most useful for familiar, clearly specified tasks; only some
  paths perform syntax checks. Inspect generated code before execution.
- Speed depends on the device; numpy is recommended.

## Privacy and safety notes

- The package contains no telemetry, user accounts, or analytics.
- The HTTP listener uses `127.0.0.1` unless configured otherwise.
- Web research can be skipped by setting `TENSEI_OFFLINE=1`.
- Learned runtime records reside in a local SQLite database below
  `TENSEI_HOME`.
- The model and data are supplied as-is; independently check important claims.
- Report security issues through the process in [SECURITY.md](SECURITY.md).

## Licensing

The project is under the MIT license. Refer to [LICENSE](LICENSE).
