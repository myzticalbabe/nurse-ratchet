# Documentation

Organised by the four [Diátaxis](https://diataxis.fr) quadrants, because the four
kinds of document answer four different questions and mixing them produces
something that does none of the jobs. Each section below names what exists today
and what does not — an empty quadrant is listed as empty rather than filled with
scaffolding.

| quadrant | the reader's question | here |
|---|---|---|
| **Tutorial** — learning | "walk me through it" | *none yet.* The closest artefact is `rt_channel.py --demo`, which runs three real turns end to end, but a tutorial is a separate job and is not written. |
| **How-to** — task | "how do I do X" | [`../README.md#quickstart`](../README.md#quickstart) — run the tests, run the channel, run the three instruments. Short on purpose. |
| **Reference** — information | "what exactly does it do" | [`reference/psyche.md`](reference/psyche.md) — module by module: functions, fields, exit codes. |
| **Explanation** — understanding | "why is it like this" | [`explanation/why-nurse-ratchet.md`](explanation/why-nurse-ratchet.md) — the design decisions and the measurements that forced them; [`explanation/live-counselors.md`](explanation/live-counselors.md) — the role this package is built for, and the six requirements it does not yet meet. |

## Reading order for a new contributor

1. [`../README.md`](../README.md) — what it is, and the limitations section first.
2. [`explanation/live-counselors.md`](explanation/live-counselors.md) — what the package
   claims to replace, and what would have to be true for that claim to hold.
3. [`explanation/why-nurse-ratchet.md`](explanation/why-nurse-ratchet.md) — why the layers are
   ordered this way, and why the safety branch is structured as it is.
3. [`reference/psyche.md`](reference/psyche.md) — the surface you will touch.
4. [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — the negative-control rule.

## Documents outside the quadrants

Some documents are governance rather than explanation, and do not fit:

- [`../DISCLOSURE_POLICY.md`](../DISCLOSURE_POLICY.md) — what ships and what never does.
- [`../SECURITY.md`](../SECURITY.md) — reporting, including behavioural safety.
- [`../PUBLIC_MANIFEST.json`](../PUBLIC_MANIFEST.json) — the machine-readable
  allowlist that the release gate enforces.
- [`../certification.json`](../certification.json) — the requirements, acceptance
  criteria and evidence behind the percentage bar in the README. `tools/certification_bar.py`
  derives the number from it, and the release gate fails when the two drift.

## A rule for this directory

Every number in these documents names the command that produced it. A figure with
no reproduction step is deleted rather than trusted — that is the same rule the
code follows, applied to prose.
