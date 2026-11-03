# Disclosure policy

What this project publishes, what it never publishes, and how the difference is
enforced rather than trusted.

## The line

**The method ships. The case does not.**

This project grew out of a forensic investigation into how a care provider
treated the people it served. The *techniques* that investigation produced —
flock-based edge accounting, tier-graded evidence, negative universes, partial
correlation networks over constructs, evaluation splits — are general, checkable
by anyone with their own data, and worth publishing. The *records* are the
private lives of identifiable people, including mental-health and tenancy
records, and publishing them would be indefensible whatever the licence says.

So the public repository contains: instruments, protocols, aggregate counts,
synthetic fixtures and citations. It does not contain the documents those
citations point at.

## Never published

| class | examples | why |
|---|---|---|
| primary records | fetched PDFs, 990 part-VII extracts, court filings | they name private individuals; a re-fetchable citation has the same evidentiary value |
| entity linkage | person-level resolution output, officer and tenant tables | linkage is itself an allegation about who is who |
| narrative findings | findings documents about an identified organisation | defamation risk is not a licence question |
| correspondence | signed instruments, emails, letters | consent was never given for publication |
| raw fetch state | `FETCH_LOG`, raw-fetch directories, unsanitised caches | provenance for a claim, not a document set |
| personal data | addresses, dates of birth, NPIs, medical details | no public interest weighs against a named individual's privacy here |

`PUBLIC_MANIFEST.json` lists these as `never_ship` globs. It is a *deny* list, so
it is backed by an allowlist: a file must be declared to ship, and an undeclared
file above 4 KB fails the gate. Deny-lists fail open; allowlists fail closed.

## What a reader can verify instead

Every claim in the method documents is reproducible from sources the reader
fetches themselves:

- the **quote, the amount, the date and the names** that make an assertion
  checkable, with the document's SHA-256 so a re-fetch can be matched byte for byte;
- the **instrument** that consumes them, which ships in full;
- the **aggregate figures**, which are counts over documents the reader can obtain.

That is the same standard this project applies to its own evidence: no raw file,
no verification; a hash plus a re-fetchable locator, verification available to
anyone, documents held by nobody.

## Enforcement

```bash
python tools/nurse_ratchet_release_gate.py --check
```

fails when: a required community file is absent, an issue template lacks the
frontmatter keys GitHub reads, a manifest path does not exist, a declared path
matches a `never_ship` rule, an undeclared file is above the size floor, a
secret-shaped string appears anywhere in the tree, or the README loses its
Limitations section.

The last one is deliberate. A public therapeutic project that quietly drops its
measured recall figure is more dangerous than one that was never published,
because a reader would trust it.

## If you believe something here should not be public

Open an issue titled `disclosure` with the path and the reason. Takedown requests
are honoured on a single maintainer's judgement, before any discussion of whether
the material was lawful to publish. No contributor's consent overrides a data
subject's objection.

## Reporting a vulnerability

See `SECURITY.md`. For anything that is a safety concern about the agent's
behaviour rather than a software defect, use the same channel and say so in the
title: behaviour reports are triaged first.
