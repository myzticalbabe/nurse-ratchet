## What this changes

<!-- One paragraph. What is true after this merge that was not before? -->

## The failing test, first

<!--
Paste the failing test and its output, before the fix. A pull request that cannot
show the gap is a pull request that cannot show it closed the gap.
-->

```text
<failing test output>
```

## The control

<!-- Which test would catch the new behaviour silently breaking later? -->

- [ ] Test added or identified: `tests/...`

## Measurement

<!--
Required for any claim of faster, safer or more accurate. Two numbers and the
machine. "Improved" is not a measurement.
-->

| before | after | machine |
|---|---|---|
|  |  |  |

## Checklist

- [ ] `python -m pytest tests/ -q` passes.
- [ ] `python tools/nurse_ratchet_release_gate.py --check` passes.
- [ ] `CHANGELOG.md` has an entry under `## [Unreleased]`.
- [ ] No new runtime dependency, or the description says why one is required.
- [ ] No evidence, name, screenshot or record of an identifiable person is added.
- [ ] No threshold, floor or penalty was changed without stating the measurement.
- [ ] The holdout split was **not** used for tuning. If new data was needed, a new
      holdout was written and this line is annotated with that fact.

## Anything you could not establish

<!--
Expected and welcome. An admitted unknown is fine; an unstated one is not.
-->
