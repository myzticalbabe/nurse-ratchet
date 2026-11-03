# Manifest notes

`PUBLIC_MANIFEST.json` is the allowlist. Nothing ships that it does not name, and
`tools/publicize.py` refuses to copy a path it cannot find there.

## Why an allowlist instead of a deny-list

A deny-list fails open. A directory added after the list was written ships by
default, and the failure is silent: the push succeeds, the artifact is public, and
nobody looks again. An allowlist fails closed, and the failure is a red gate
before anything leaves the machine.

## The layout

The source lives in a larger monorepo where the package is `PSYCHE`. The public
package is `nurse_ratchet.psyche`. Two consequences, both mechanical:

- **Files are copied, not moved.** The monorepo keeps working; the public tree is
  a derived artifact and can be regenerated at any time.
- **Imports are rewritten, in three forms.** `from PSYCHE.affect import clamp`
  becomes `from nurse_ratchet.psyche.affect import clamp`; `import PSYCHE as pkg`
  becomes `import nurse_ratchet.psyche as pkg`; `from PSYCHE import x` becomes
  `from nurse_ratchet.psyche import x`. The third form was added after an
  instrument began resolving its data from the installed package, matched neither
  of the first two, and killed both instruments in the public tree while the
  source tree kept working. A verbatim copy would install cleanly
  and fail on first import — in the published artifact, after the push. So
  `tools/publicize.py` verifies the rewrite by importing the public package in a
  fresh subprocess with only the public tree on `sys.path`, and exits non-zero if
  that import fails.

The `sys.path.insert(0, .../src)` bootstrap in the copied tools is removed rather
than rewritten. In the public tree the package is installed; a bootstrap pointing
at a directory that does not exist is a lie that happens to work on the author's
machine.

## What never ships, and why

`never_ship` and `deny_substrings` hold back raw forensic evidence: source
documents, entity-resolution output, correspondence, and rendered findings about
identified organisations and people. This project's *method* is publishable; the
allegations inside its original case are not, and no licence makes republishing
primary records about named people in mental-health, tenancy and employment
matters lawful or decent.

The instruments do not depend on that material. Each one runs against data the
reader supplies, which is why a reader can verify the method without receiving the
case: ship the quote and its SHA-256, and let a verifier re-fetch.

## Regenerating

```bash
python tools/publicize.py          # copy + rewrite + verify
python tools/publicize.py --check  # verify only, write nothing
python tools/publicize.py --clean  # remove generated files
python tools/nurse_ratchet_release_gate.py --check
```
