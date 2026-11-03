# Tutorial: from a clone to a running turn

This walkthrough is not illustrative — every command below was run, and the
output blocks are copied from that run. Where a number is surprising it is left
in, because a tutorial that shows only the happy path teaches a reader to trust
output that has not been checked.

Time: about two minutes. Nothing here needs a network, an API key or a model.

---

## 0. Materialise and install

The public tree is generated from `PUBLIC_MANIFEST.json`; `nurse_ratchet/psyche/*` does
not exist in the source tree. Materialising is a separate step from installing on
purpose — it is the step where imports get rewritten, and having it fail loudly
before `pip install` is the point.

```bash
python tools/publicize.py
python -m pip install -e ".[dev]"
```

`publicize.py` ends with a verification, not a summary line: it imports
`nurse_ratchet.psyche.rt_agent` in a subprocess whose only path entry is this tree. If the
rewrite were wrong, this is where it would fail — not in a user's first `import`.

## 1. One turn

```bash
python - <<'PY'
from nurse_ratchet.psyche.network import PersonNetwork, bridge_name
from nurse_ratchet.psyche.intuition import IntuitionIndex
from nurse_ratchet.psyche.rt_agent import TherapeuticLoop

net = PersonNetwork()
loop = TherapeuticLoop(net, IntuitionIndex(net))
for line in ("work has been relentless and I am not sleeping",
             "I keep thinking about ending things"):
    turn = loop.turn(line)
    print("%-12s %-10s %s" % (turn.risk.risk, turn.stance, turn.message[:64]))
print("bridge:", bridge_name(), "| stamped on the graph:", net.activation_source)
PY
```

```text
low          consolidate Notice what you just did: you stayed with avoidance instead of l
crisis       safety     What you just said matters more than anything else in this conve
bridge: fitted-ridge | stamped on the graph: fitted-ridge
```

Two things to notice. The second turn routes to **safety** and no other stance is
considered — crisis is checked before anything else in the turn, which is why a
turn can never be "validated" into a crisis. And `bridge` tells you which
affect→construct map produced the graph: `fitted-ridge` when
`nurse_ratchet/psyche/data/affect_bridge.json` is present, `hand-map` otherwise. A graph
built under one map and read as if it came from the other is two different claims
about one person, so the graph carries the label.

## 2. The live channel

`rt_channel` speaks newline-delimited JSON over stdio: one line in, one flushed
line out, per-turn latency in the payload. It is the shape a realtime front end
needs, and it is testable without one.

```bash
printf '%s\n' '{"id":"t1","text":"I have not slept in three days"}' \
  | python -m nurse_ratchet.psyche.rt_channel
```

```text
{"id": "t1", "stance": "consolidate", "message": "Notice what you just did: you stayed with avoidance instead of leaving it. That is the part worth remembering.", "focus": "avoidance", "risk": "low", "risk_reasons": ["no intent language and no collapse markers in this reading"], "latency_ms": 1.5762, "within_budget": true, "path": "deliberate-after-miss", "prototype": null, "rationale": "utility=0.46 (approach=0.00 self_worth=0.05, nothing acute); risk=low; intuition=deliberate-after-miss/no-prototype"}
```

A malformed line answers with an error record carrying the same `id` and the
stream stays open. Silence would be indistinguishable from a crash, and a client
cannot tell the difference either.

## 3. Grade the safety router — and read the spread

```bash
python tools/triage_eval.py --split dev
python tools/triage_eval.py --split holdout2
python tools/triage_eval.py --split holdout3
```

```text
$ python tools/triage_eval.py --split dev
  confusion  TP 13  FP 0   TN 17  FN 0
  recall 1.0  precision 1.0  specificity 1.0  accuracy 1.0

$ python tools/triage_eval.py --split holdout2
  confusion  TP 10  FP 0   TN 12  FN 2
  recall 0.83  precision 1.0  specificity 1.0  accuracy 0.91

$ python tools/triage_eval.py --split holdout3
  confusion  TP 2   FP 2   TN 10  FN 9
  recall 0.18  precision 0.5  specificity 0.83  accuracy 0.52
```

This is the most important number in the project and the reason the README leads
with limitations rather than features. Read it as follows:

- **dev** is what the router was tuned against. A high score there is arithmetic,
  not evidence.
- **holdout2** and **holdout3** were written by the same author, on the same day,
  and differ by a wide margin. That spread is the actual finding: it says the
  single number does not exist yet, and that a lexical detector's recall depends
  more on who wrote the test sentences than on whether it works.
- Every run prints its own provenance line. The instrument is built so it cannot
  report a score without also reporting what the score does not mean.

## 4. Confirm the fitted bridge is the bridge you think

```bash
python tools/fit_affect_bridge.py --check
```

```text
shipped vs fresh fit: max drift 0.00e+00 ; recovery z 3.12 -> OK
```

`--check` compares the shipped coefficients to a fresh fit at the tool's own
default seed. Given the seed the fit is deterministic, so **any** drift means a
human edited the numbers. Comparing against the ground truth instead would let a
plausible edit pass, which is the check you actually want to fail.

The recovery figure is the estimator's own sampling error, not a hand-picked
tolerance: `se_i = sigma * sqrt((X'X)^-1_ii)`, and a correct fit lands within a
few `se`. The first version of this tool used a fixed tolerance and failed a
correct estimator on its first run — the fix was to ask the estimator how
precise it is instead of deciding for it.

## 5. Gate the paperwork

```bash
python tools/nurse_ratchet_release_gate.py --check
```

```text
nurse-ratchet publication gate -- <path to this tree>
  required_files     ok
  readme_disclosure  ok
  issue_templates    ok
  manifest_paths     ok
  denied_paths       ok
  undeclared_files   ok
  secrets            ok

PASS: 0 failure(s)
```

The gate fails closed: undeclared paths, missing community files, a secret in any
text file, or a README that has lost its Limitations section. It publishes
nothing — it only refuses.

---

## What you have not verified

Nothing here shows the loop helps anyone. The corpus is invented utterances
labelled by the same author who wrote the detector; the bridge is fitted against a
synthetic ground truth; and no construct data from real people exists in this
project at all (`tools/psyche_fit_pams.py` exits 2 for exactly that reason, and
declines rather than substituting tags for constructs). The tests confirm the
instruments measure what they claim to measure. They cannot confirm the thing
being measured is the right thing.

Read `DISCLOSURE_POLICY.md` and the README's Limitations section before using any
of this near a person.
