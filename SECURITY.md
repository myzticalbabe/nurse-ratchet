# Security policy

## Supported versions

`0.1.x`, which is **pre-publication**. There is no supported release yet; this
file exists so that the channel is defined before anyone needs it.

## Reporting

**Do not open a public issue for a vulnerability or a safety failure.**

Use GitHub's private vulnerability reporting on this repository (Security →
Report a vulnerability). If that is unavailable, open an issue containing only
the words `security contact requested` and nothing else — no detail, no
reproduction — and a maintainer will open a private channel.

Include, at minimum:

- what an attacker or a user can make the software do that they should not;
- the version or commit;
- whether a **person** could be harmed by it, not just a process.

We acknowledge within 72 hours, and aim to ship a fix or a documented mitigation
within 30 days for anything that can harm a user.

## Scope, in the order we care about it

1. **Behavioural safety.** Anything that makes the agent's crisis routing weaker
   than documented is a security issue here, not a bug. That includes a change
   that raises the fast-path threshold in a way that routes an intent statement to
   an ordinary stance, a prompt or input that suppresses the triage branch, and any
   path where a resource message can be replaced by generated text.
2. **Data handling.** The agent holds a person's psychological graph. Leakage
   vectors — logs, artefacts, temporary files, the channel's stdout — are in scope.
   `SessionChannel` writes responses to the stream it is given; it must never write
   a person's construct values anywhere else, and a report showing otherwise is
   high severity.
3. **Secrets and supply chain.** This project ships no runtime dependencies, so a
   dependency appearing at all is worth reporting. Note that the release gate
   scans for secret-shaped strings and refuses to publish when it finds one.
4. **Denial of service on the channel.** A malformed line must not end a session;
   an unbounded line must not be read into memory. Both are tested, and a
   regression is in scope.

## Out of scope

- **The agent giving bad advice.** It is not a clinician and does not claim to be;
  the model is a mechanism, and its measured weakness is published in the README.
  If it is *worse* than the README says, that is in scope — say so.
- **The holdout recall figure.** 0.33 is documented, not hidden. A report that it
  is low is not a vulnerability; a report that a *deployment* relies on it alone
  is, and the answer will be that this is not permitted.
- **Missing hardening on a local, single-user script** with no network listener.
  `rt_channel` speaks on stdio; if you have exposed it to a network, that is the
  finding, and we will document it rather than defend it.
- Findings that require a hostile operator who can already read the person's store
  and edit the code.

## A note on scope creep in the other direction

If a report shows the safety branch can be outbid — that a crisis verdict can be
overridden by a stance utility — that is the highest-severity finding this project
can receive, because the entire design rests on it being impossible. Send it
privately, and know that it is the one issue that stops a release rather than
being scheduled into one.
