# Contributing to Project Nurse Ratchet

## The one rule

**Bring a negative control.** A claim that cannot be shown false is not accepted,
however true it sounds. In practice:

> Every test that shows a thing working ships with a test that would catch it
> failing.

Examples from this repository, so the standard is concrete rather than aspirational:

| claim | control that must exist |
|---|---|
| the estimator recovers a planted dependency | an independent pair gets **no** strong edge |
| idioms do not fire the crisis router | `"killing time"`, `"dead tired"` return risk `low` |
| an unseen pattern does not take the fast path | 100 unfamiliar calls, **0** fast-path answers |
| the evaluation instrument measures the router | a corpus the router *cannot* see scores **recall 0.0** |
| the PAMS probe refuses rather than guesses | a memory-shaped store exits **2** with the reason |

If you cannot write the control, say so in the pull request and explain what
evidence would settle it. An admitted unknown is welcome; an unstated one is not.

## Getting set up

```bash
git clone <this repository>
cd nurse-ratchet
python -m pytest tests/ -q
```

Python 3.10+. No third-party runtime dependencies: PSYCHE is standard library by
design, so a reviewer can read the whole model in an afternoon. Do not add a
dependency for something a hundred lines of Python does correctly — if you think
one is justified, open an issue first with the measurement that motivates it.

## What a pull request needs

1. **A failing test first**, in the PR description, showing the defect or the gap.
2. **The fix**, with the smallest surface that addresses it.
3. **The control**, as above.
4. **A measurement**, not an adjective. "Faster" needs two numbers and the machine
   they came from; "safer" needs a case that used to pass and now fails.
5. **A changelog entry** under `## [Unreleased]` in `CHANGELOG.md`, using one of
   Added / Changed / Deprecated / Removed / Fixed / Security.

## What gets rejected

- A safety change with no test proving the unsafe path is now unreachable.
- Tuning a model or router against the **holdout** split. If you need new data to
  fix a miss, write a fresh holdout and say that you did.
- Quiet changes to a threshold, a floor or a penalty. These are claims about a
  store or a population; state the measurement that moved them.
- Removing a limitation from the README. `tools/nurse_ratchet_release_gate.py --check`
  fails when the disclosure is missing, and that failure is not to be worked around.
- Adding an evidence file, a screenshot of a record, or a name. See
  `DISCLOSURE_POLICY.md`; the gate will refuse it, and the refusal is correct.

## Style

- Comments explain **why**, and prefer the measurement: *"0.62 requires support of
  about four observations"* over *"threshold chosen empirically"*.
- No imports inside functions: a module that cannot fail at import time fails at
  the worst possible moment instead.
- No `except: pass`. If a failure is expected, name it and record it; if it is
  unexpected, let it travel.
- Public functions carry docstrings that state what the function does **not** do,
  where that is the interesting part.

## Commits

Conventional-ish, imperative, and the body says what was measured:

```
network: discount similarity by coordinate coverage

Plain cosine over the union scored an exact 2-of-4 instance at 0.76 and the fast
path fired 0 times in 100 calls. Matching on the measured subset with a
sqrt(coverage) discount restores the fast path for 4-of-6 coverage while a single
coordinate stays below the match floor. Control: tests/test_psyche_intuition.py.
```

## Review

One maintainer. Expect the first question to be "what would show this is wrong?".
Expect it to be asked about your own PR and about the reviewer's, and expect a
review to be withdrawn with a measurement rather than defended with a preference.

## Code of conduct

`CODE_OF_CONDUCT.md` applies to issues, pull requests and any project space.
Reports go to the address in `SECURITY.md`. Behaviour that endangers a user of
this software is treated as a security report, not a moderation matter, and is
triaged first.
