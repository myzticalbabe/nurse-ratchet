# Reference — the Nurse Ratchet stack

Information only: what exists, what it takes, what it returns. Rationale lives in
[`../explanation/why-nurse-ratchet.md`](../explanation/why-nurse-ratchet.md).

Dependency order is the order below. Nothing lower imports anything higher.

---

## `nurse_ratchet/psyche/network.py` — the construct graph

```python
PersonNetwork(nodes=None, ridge=0.25)
```

| member | signature | notes |
|---|---|---|
| `observe` | `(values: dict[str, float], at_s: float = 0.0)` | folds one reading in; unknown keys add nodes; history bounded to 500 |
| `fit_edges` | `(ridge: float \| None = None) -> list[Edge]` | ridge-regularised partial correlations; needs ≥3 observations and ≥3 nodes, else returns `[]` and records why |
| `edges` | `() -> list[Edge]` | sorted by descending absolute weight |
| `propagate` | `(activation, steps=1, gain=0.6) -> dict` | one or more message-passing layers |
| `centrality` | `() -> dict[str, dict]` | `strength`, `betweenness`, `edges`, `support` per node |
| `explain` | `(node, top_k=3) -> list[dict]` | incoming paths with `path_strength` |
| `diagnostics` | `() -> dict` | counts, ridge, last 20 recorded errors |

`Edge` fields: `a`, `b`, `weight` (partial correlation, signed), `support`.
`EDGE_FLOOR = 0.05`: weaker edges are not stored.
`activation_from_pad(pad, families=("anxiety", "sadness"))` maps an affect reading
onto construct values — the hand-mapped bridge, named as the weakest assumption.

## `nurse_ratchet/psyche/intuition.py` — compiled inference

```python
IntuitionIndex(network, min_support=2, match_floor=0.55)
```

| member | signature | returns |
|---|---|---|
| `absorb` | `(activation, name=None, at_s=None)` | the `Prototype` updated or created |
| `read` | `(cues) -> Reading` | fast path; `known=False` when nothing clears `match_floor` |
| `deliberate` | `(cues, steps=2) -> Reading` | runs the graph; always answers |
| `read_or_think` | `(cues, threshold=0.62) -> Reading` | fast if `known` and confident, else deliberate |
| `resolve` | `(reading, outcome, correct, at_s=None)` | files the outcome; **does not** edit the prototype |
| `calibration` | `() -> dict` | `resolved`, `brier`, `accuracy`, `mean_confidence`; `brier=None` at zero resolutions |
| `agreement` | `(cues) -> dict` | fast vs slow prototype, `agree`, both latencies, ratio |
| `recommend_threshold` | `() -> dict` | `threshold=None` below 8 resolutions |

`Reading` fields: `prototype`, `confidence`, `similarity`, `support`, `known`,
`latency_us`, `path`, `profile`.
`confidence = similarity × (1 − e^(−support/4))`; `similarity` is the observed-key
cosine multiplied by `sqrt(coverage)`.

## `nurse_ratchet/psyche/rt_agent.py` — the loop

```python
TherapeuticLoop(network, index, pad=(0,0,0), baseline=(0,0,0),
                decay_rate=0.15, budget_ms=50.0, threshold=0.62, audit_limit=64)
```

`turn(text="", appraisal=None, dt_s=1.0, observe=True) -> TurnResponse`

Order, fixed: decay → appraisal blend → graph update → **triage** → stance.
A `crisis` verdict returns the `safety` stance and no other stance is scored.

| symbol | meaning |
|---|---|
| `STANCE_TEMPLATES` | `safety`, `validate`, `regulate`, `reframe`, `skills`, `consolidate` |
| `RISK_LEVELS` | `low` < `monitor` < `elevated` < `crisis` |
| `LOW_DOSE_STANCES` | `validate`, `regulate`, `consolidate` — the only eligible stances under `elevated` |
| `LEARNING_WINDOW_AROUSAL = 0.72` | above this, `regulate` pre-empts `skills` and `reframe` |
| `CRISIS_CUES` / `CRISIS_PATTERNS` | exact phrases / paraphrase families |
| `CRISIS_EXCLUSIONS` | idioms that must not fire (`"killing time"`, `"dead tired"`) |
| `triage(text, activation) -> Triage` | `risk`, `reasons` (never empty), `matched` |

`triage` reads three channels and keeps the highest verdict: concept-coherence
cues, the phrase families above, and `constructions.analyse`. The third exists
because a statement can name no crisis vocabulary and still say the self is gone
from the future (`"there's no version of next year that has me in it"`).

`Triage` attribution rules: intent language attributed to another person, framed
in the past, or inside a quotation → `monitor`, not `crisis`. A first-person
marker overrides the guard.

## `nurse_ratchet/psyche/rt_channel.py` — the channel

```python
SessionChannel(loop, max_message_chars=400)
```

Wire protocol, newline delimited, one response per request line, flushed:

```json
{"id": 1, "text": "...", "appraisal": {"desirability": -0.7}, "dt_s": 1.0}
{"id": 1, "stance": "validate", "risk": "low", "latency_ms": 0.031,
 "within_budget": true, "path": "intuition", "prototype": "threat-loop",
 "message": "...", "focus": "threat appraisal", "rationale": "..."}
```

- Missing `id` defaults to the line number.
- Malformed JSON → `{"id": null, "error": "line N is not JSON: ..."}`; the
  session continues.
- Bad field types → an error record, never an exception.
- A message longer than `max_message_chars` is truncated and marked `[truncated]`.
- `MAX_LINE_BYTES = 65536`; a longer line is answered with an error, not read.

CLI: `--demo [--turns N]` runs a self-contained script; default mode serves stdio
with an *unfitted* graph and says so on stderr.

## `nurse_ratchet/psyche/constructions.py` — construction grammar

```python
analyse(text) -> ConstructionReport   # .frames, .foreclosed, .self_subject
```

A frame is a subject, a verb sense, an object and what the sentence forecloses.
`SELF` is the sentinel subject for first person. The report drives the third
triage channel: foreclosure of the self plus a third-person subject is not the
same evidence as the self as agent.

## `nurse_ratchet/psyche/elicitation.py` — the construct battery

```python
new_session(seed=None) -> Session
score_session(answers, pad, *, taken_at, order=None, note="") -> Record
```

`INSTRUMENT_VERSION = "psyche-constructs-1"`. Ten constructs, three items each,
scale 0-4 with midpoint 2, **one reverse-scored item per construct**. Construct
scores are on -1..1 with the midpoint at 0.

| symbol | meaning |
|---|---|
| `ITEMS` | 30 `Item(key, construct, text, reverse)` |
| `CONSTRUCTS` | the same ten nodes `network.DEFAULT_CONSTRUCTS` carries |
| `AFFECT_ITEMS` | three PAD sliders, -1..1, taken in the same session |
| `Record.digest` | sha256 over the scored content, taken at scoring time |
| `Record.stored_digest` | the digest as written, so a hand-edited store is detectable |
| `homogeneity(records)` | forward-vs-reverse gap per construct; high means re-take |
| `IncompleteSession` | raised instead of renormalising a partial session |

## Instruments

| tool | exit codes | what it establishes |
|---|---|---|
| `tools/triage_eval.py` | 0 = ran, 1 = below `--min-recall` | confusion matrix, per-category recall, dev/holdout split, misses with false negatives first |
| `tools/psyche_fit_pams.py` | 0 = fitted, 2 = no construct signal or <3 readings, 1 = error | whether a store carries per-construct readings at all; refuses rather than proxying |
| `tools/elicit.py` | 0 = ok, 2 = refused (incomplete session, no records, failed digest) | administers the battery and appends to `~/.psyche/elicitations.jsonl`; `stats` reports the reverse-vs-forward gap |
| `tools/fit_affect_bridge.py` | 0 = fitted, 1 = recovery failed, 2 = refused (too few records, flat construct, mixed instrument) | `--check` verifies the shipped synthetic fit; `--from-records` fits a per-person bridge and refuses below 50 sessions |
| `tools/publicize.py` | 0 = materialised and verified, 1 = verification failed | that the public tree imports and that both instruments run in it |
| `tools/nurse_ratchet_release_gate.py` | 0 = publishable, 1 = blocked | community-file standard, manifest allowlist, evidence deny-list, secret scan, required disclosures |

`triage_eval` corpus format: JSONL, one `_meta` row with `authored`, then rows of
`text`, `expect_crisis`, `category`, optional `split` (`dev` default, `holdout`
for data written after the last change).

## Thresholds and floors, with their provenance

| constant | value | where it came from |
|---|---|---|
| `EDGE_FLOOR` | 0.05 | below this an edge is shrinkage noise; keeping it makes centrality meaningless |
| `DEFAULT_RIDGE` | 0.25 | enough to invert degenerate covariance; not fitted |
| `MIN_SUPPORT` | 2 | one occurrence is not a pattern |
| `MATCH_FLOOR` | 0.55 | below this the answer is "not seen", not a weak guess |
| `DEFAULT_THRESHOLD` | 0.62 | reached at support ≈ 4 on full coverage |
| `LEARNING_WINDOW_AROUSAL` | 0.72 | clinical convention, **not** measured here — flagged as such in the source |
