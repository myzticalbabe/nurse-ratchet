# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Same day as 0.1.0, and recorded separately because each entry changes a number or
a claim that the 0.1.0 text states.

### Added

- **`certification.json`, `tools/certification_bar.py` -- a computed certification
  bar.** The six requirements in `docs/explanation/live-counselors.md` are stored
  as requirements, acceptance criteria and evidence, and the percentage is derived
  from them: **22.6%** at this commit, 4 of 19 criteria, 0 of 6 required
  requirements. The README block is generated (`--write`) and the release gate
  fails when it drifts (`--check`), so the number cannot be typed and cannot be
  remembered. Two readings stay separate on purpose: the percentage is weighted
  progress, `deployable` is a gate that stays **no** until every required
  requirement is fully met. A `done` criterion must cite a path that exists, so
  the bar cannot outlive the evidence behind it; a misspelled key is refused rather
  than silently read as "not done". Certificates actually held (SOC 2, ISO 27001,
  HIPAA attestation) go in `held`: they are printed under the bar and deliberately
  do not raise it, because they audit the process, not the clinical claim.
- **Package renamed `eliza` → `nurse_ratchet`.** Distribution `eliza` →
  `nurse-ratchet`, console script `eliza-psyche` → `nurse-ratchet-psyche`, gate
  `eliza_release_gate.py` → `nurse_ratchet_release_gate.py`, doc `why-eliza.md` →
  `why-nurse-ratchet.md`. **Correction (2026-11-02): the directory rename
  `Project_ELIZA` → `Project_Nurse_Ratchet` that accompanied this was an agent
  error.** ELIZA and Nurse Ratchet are two different projects — ELIZA is the
  forensic investigation suite, Nurse Ratchet is the therapeutic health agent —
  and the rename wrongly merged them. `Project_ELIZA` is restored as its own tree;
  only the package rename above was correct. References to Weizenbaum's 1966 ELIZA
  stay where they are factual: it is a real citation and a real demonstration of
  the effect this project is built around.
- `src/PSYCHE/elicitation.py`, `tools/elicit.py` — the construct battery, and the
  instrument that administers it. Ten constructs, three items each, one
  reverse-scored item per construct so acquiescence is detectable instead of
  reading as a perfect profile; affect is taken as three PAD sliders in the same
  session, because a bridge between affect and constructs needs both halves
  measured in the same moment. Records append to `~/.psyche/elicitations.jsonl`
  with a content hash taken at scoring time. This is the missing half of the
  affect→construct bridge: the coefficients were fitted against a synthetic truth
  because no construct reading existed anywhere in this project, and the reason
  was the absence of an instrument, not of an algorithm.
- `tools/psyche_fit_pams.py` probes the elicitation store **first** and fits the
  construct graph from it. Three sessions are enough for edges; below that it
  prints the node count and zero edges, which is the honest reading. A store that
  is absent now says so, and a refusal lists it: a refusal that omits the one
  source that would answer teaches the reader the project has nowhere to put a
  measurement.
- `tools/fit_affect_bridge.py --from-records` fits the bridge against elicited
  records and **refuses** below 50 sessions from one instrument version, on a
  constant construct, or across mixed instrument versions. Its coefficients
  describe a different model from the synthetic fit (no appraisal-family
  features), and the tool says so rather than letting the two be compared.
- `src/PSYCHE/constructions.py` — construction-grammar risk detection: who a
  sentence makes an agent, what action is foreclosed, and whether the self is the
  subject. It is a third channel in `rt_agent.triage`, alongside the concept-family
  cues and the phrase list.
- `tools/fit_affect_bridge.py` — fits the affect→construct bridge by ridge
  regression and verifies **coefficient recovery** against a known synthetic
  ground truth, judged against each coefficient's own standard error rather than
  a hand-picked tolerance. Reports divergence from the hand map (mean |delta|
  0.135, top-construct identity flips on 42.7% of grid inputs) and how often the
  collapse detector changes verdict between the two bridges (10.1%).
- `src/PSYCHE/data/affect_bridge.json` — the fitted coefficients, with the
  synthetic-ground-truth provenance in the file itself.
- `Project_Nurse_Ratchet/tools/publicize.py` — materialises the public tree from the
  allowlist and **verifies** it by running the package and both instruments in a
  subprocess, not by checking that files were copied.
- `pyproject.toml`, `.github/workflows/ci.yml`, `docs/tutorial.md`,
  `MANIFEST_NOTES.md` — the package is installable and the tutorial's commands
  and output blocks come from an actual run.

### Changed

- **Crisis detection replaced.** Exact phrases plus four fitted pattern families
  were replaced by concept-coherence scoring over clinical item families. A fresh
  holdout went from recall 0.00 to 0.83; a third holdout, written after the
  detector was frozen, scored 0.18. The README now leads with the spread rather
  than a single figure, because no single figure is honest.
- `network.activation_from_pad` reads the fitted coefficients when present and
  falls back to the hand map when not. `PersonNetwork` stamps
  `activation_source`, so a graph carries the map that produced it.
- Instruments resolve the corpus and the bridge from the **installed package**
  rather than `ROOT/src/...`, which did not exist in the public tree.

### Fixed

- `publicize.py` rewrote two of the three ways a module can be imported. Once an
  instrument resolved its data from the installed package — `import PSYCHE as
  _psyche_pkg` — that line matched neither pattern, and both instruments died in
  the public tree with `ModuleNotFoundError: No module named 'PSYCHE'` while the
  source tree kept working. Verification caught it; the rewrite looked complete.
- `test_psyche_rt_channel.py` built `PYTHONPATH` by walking up a fixed number of
  directories, which is one level too many for a two-level package. It now derives
  the path from the top-level package, so the same file is correct in both trees.
- `nurse_ratchet_release_gate.py` counted only manifest *sources* as declared, so every
  materialised tree failed its own gate. A declared destination is declared.
- `fit_affect_bridge.py` folded to `publicize.py`, `triage_eval.py`,
  `test_psyche_affect.py` and `test_psyche_rt_channel.py` — all four resolved
  paths by source layout and failed in a public checkout.
- `test_no_demographic_inputs` scanned a hard-coded list of six modules and had
  gone stale; it now discovers the package's modules, so it covers the four added
  since the list was written.

## [0.1.0] - 2026-11-01

### Added

- `nurse_ratchet/psyche/network.py` — construct graph. Nodes are constructs and observable
  states; edges are ridge-shrunk partial correlations estimated from observations
  and editable by hand; one GNN message-passing layer with symmetric degree
  normalisation. Centrality carries the edge support behind each row.
- `nurse_ratchet/psyche/intuition.py` — compiled inference. Prototypes with support counts,
  `read()` / `deliberate()` / `read_or_think()`, a resolution ledger and a Brier
  score reported with the count it rests on. Resolving a reading never edits the
  prototype, so a wrong intuition stays wrong and stays measurable.
- `nurse_ratchet/psyche/rt_agent.py` — the realtime loop. Six stances, risk triage before
  stance scoring, a receptivity gate that keeps skills work out of a state outside
  the learning window, and a dose cap on elevated risk.
- `nurse_ratchet/psyche/rt_channel.py` — newline-delimited JSON over stdio, flushed per
  turn, with per-turn budget reporting and error records that never end a session.
- `tools/triage_eval.py` — crisis-router evaluation with dev/holdout splits, a
  per-category breakdown, and false negatives printed before false positives.
- `tools/psyche_fit_pams.py` — probes a store for construct-bearing readings and
  **refuses** to fit when none exist. Exit code 2 is a result, not a failure.
- `tools/nurse_ratchet_release_gate.py` — publication gate: community-file standard,
  manifest allowlist, evidence deny-list, secret scan, required disclosures.
- 76 tests across seven files. Every claim of a capability ships with a control
  able to show it false.

### Changed

- Crisis routing matches **patterns**, not only exact phrases, and downgrades to
  `monitor` when intent language is attributed to another person, framed in the
  past, or quoted. Motivation: an evaluation measured recall 0.76 with three
  euphemism misses and five false positives.
- Similarity matching runs on measured coordinates with a `sqrt(coverage)`
  discount instead of cosine over the union, which had made the fast path
  unreachable for exact partial matches.

### Fixed

- Elevated risk applied a 0.15 penalty that a change-work stance could outbid
  (0.75 versus 0.67). The dose is now capped: only low-dose stances are eligible.
- `stats()` mixed two denominators — session turn count against audit-window
  stance counts — so a 200-turn session appeared to have lost turns.

### Security

- The safety branch is asserted to be un-outbiddable by construction, with a test
  that supplies an input which would otherwise select a skills intervention.
- The publication gate refuses to ship a tree containing secret-shaped strings and
  refuses to publish while the README's Limitations section is missing.

### Known limitation

- Crisis-router holdout recall was 0.33 at this release (dev 1.00, fitted); the
  detector was replaced afterwards — see Unreleased. Precision on holdout
  is 1.00. This is documented in the README, asserted by a test, and is a release
  blocker rather than a backlog item.

[Unreleased]: https://example.invalid/nurse_ratchet/compare/0.1.0...HEAD
[0.1.0]: https://example.invalid/nurse_ratchet/releases/tag/v0.1.0
