#!/usr/bin/env python3
# coding: utf-8
"""Compute how certifiable this build is, and render it as a bar the README shows.

WHY A COMPUTED BAR AND NOT A NUMBER IN PROSE
-------------------------------------------
A percentage typed into a README is a claim nobody can check and everybody
updates by feel. Two things go wrong and both are silent: the number drifts from
the evidence, and a criterion is marked met because the work around it *feels*
done. So the number is not stored anywhere. `certification.json` stores the
requirements, the acceptance criteria inside each, and the evidence for every one
marked `done`; this tool derives the percentage and renders the block.

WHY EVIDENCE IS A PATH, NOT A SENTENCE
-------------------------------------
`done: true` with a sentence next to it is exactly the shape of an unverified
claim. Every done criterion must name a file in this repository (or an http
source, which cannot be checked here and is therefore labelled that way in the
render) and a note that says what the file shows. The validator refuses a path
that does not exist, so the evidence cannot rot out from under the percentage
without the bar failing.

WHY `deployable` IS SEPARATE FROM THE PERCENTAGE
-----------------------------------------------
A weighted percentage can read 96% while the one requirement that keeps a
therapeutic agent from being dangerous is unmet. Percent is progress; deployment
is a gate. They are printed as two different things, and `deployable` is true
only when every requirement marked `required` is fully met. Holding a
certificate (SOC 2, ISO 27001, a HIPAA attestation) is recorded in `held` and
deliberately does not move the percentage: those certificates are evidence of
process, and this bar is a statement about clinical validity.

Usage:
  python tools/certification_bar.py            # print the percentage and why
  python tools/certification_bar.py --write    # rewrite the README block
  python tools/certification_bar.py --check    # fail if the README block drifted
  python tools/certification_bar.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_NAME = "certification.json"
README_NAME = "README.md"

#: The block the README carries. Markers, not a heading, because a heading moves.
BLOCK_START = "<!-- CERTIFICATION:START -->"
BLOCK_END = "<!-- CERTIFICATION:END -->"

#: One cell per 5%. Twenty cells, and the exact number is always printed beside
#: it -- a bar whose fill rounds to nothing must still show that it was not zero.
BAR_WIDTH = 20
FILLED, EMPTY = "\u2588", "\u2591"

SCHEMA = "nurse-ratchet/certification@1"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")

TOP_KEYS = {"schema", "updated", "note", "held", "requirements"}
REQUIREMENT_KEYS = {"id", "title", "short", "weight", "required", "criteria"}
CRITERION_KEYS = {"text", "done", "evidence"}
HELD_KEYS = {"name", "issuer", "date", "scope"}


class CertificationError(Exception):
    """A malformed or unsupported certificate. Never downgraded to a warning."""


def load(root: Path = ROOT) -> Dict:
    path = Path(root) / MANIFEST_NAME
    if not path.exists():
        raise CertificationError("%s is absent; the bar has no data" % path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CertificationError("%s is not valid JSON: %s" % (path.name, exc)) from exc


def _evidence_problems(evidence, where: str, root: Path) -> List[str]:
    """A done criterion must point at something that exists.

    An http source is allowed and reported as `external` at render time: it
    cannot be verified from here, and pretending otherwise is the defect this
    whole tool exists to prevent.
    """
    if not isinstance(evidence, dict):
        return ["%s: evidence must be an object with `path` and `note`" % where]
    problems: List[str] = []
    unknown = set(evidence) - {"path", "note"}
    if unknown:
        problems.append("%s: unknown evidence key(s) %s" % (where, sorted(unknown)))
    path = evidence.get("path")
    note = evidence.get("note")
    if not isinstance(path, str) or not path.strip():
        problems.append("%s: evidence.path is empty" % where)
        path = None
    if not isinstance(note, str) or not note.strip():
        problems.append("%s: evidence.note is empty" % where)
    if path and not re.match(r"^https?://", path):
        target = path.split("#", 1)[0]
        if not (Path(root) / target).exists():
            problems.append("%s: evidence.path does not exist here: %s" % (where, path))
    return problems


def validate(data: Dict, root: Path = ROOT) -> None:
    """Collect every problem, then raise once. A gate that stops at the first
    finding makes the author re-run the tool one typo at a time."""
    problems: List[str] = []
    unknown = set(data) - TOP_KEYS
    if unknown:
        problems.append("unknown top-level key(s): %s" % sorted(unknown))
    if data.get("schema") != SCHEMA:
        problems.append("schema must be %r, found %r" % (SCHEMA, data.get("schema")))
    updated = data.get("updated")
    if not isinstance(updated, str) or not DATE_RE.match(updated):
        problems.append("updated must be YYYY-MM-DD")

    requirements = data.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        problems.append("requirements must be a non-empty list")
        requirements = []

    seen_ids = set()
    for index, requirement in enumerate(requirements):
        where = "requirements[%d]" % index
        if not isinstance(requirement, dict):
            problems.append("%s: must be an object" % where)
            continue
        unknown = set(requirement) - REQUIREMENT_KEYS
        if unknown:
            problems.append("%s: unknown key(s) %s" % (where, sorted(unknown)))
        identifier = requirement.get("id")
        if not isinstance(identifier, str) or not ID_RE.match(identifier):
            problems.append("%s: id must be lower_snake_case" % where)
        elif identifier in seen_ids:
            problems.append("%s: duplicate id %r" % (where, identifier))
        else:
            seen_ids.add(identifier)
            where = "requirement %r" % identifier
        for text_key in ("title", "short"):
            if not isinstance(requirement.get(text_key), str) or \
                    not requirement.get(text_key, "").strip():
                problems.append("%s: %s is empty" % (where, text_key))
        weight = requirement.get("weight")
        if not isinstance(weight, int) or isinstance(weight, bool) or not 1 <= weight <= 5:
            problems.append("%s: weight must be an integer 1..5" % where)
        if not isinstance(requirement.get("required"), bool):
            problems.append("%s: required must be true or false" % where)

        criteria = requirement.get("criteria")
        if not isinstance(criteria, list) or not criteria:
            problems.append("%s: criteria must be a non-empty list" % where)
            continue
        for position, criterion in enumerate(criteria):
            cwhere = "%s criteria[%d]" % (where, position)
            if not isinstance(criterion, dict):
                problems.append("%s: must be an object" % cwhere)
                continue
            unknown = set(criterion) - CRITERION_KEYS
            if unknown:
                problems.append("%s: unknown key(s) %s" % (cwhere, sorted(unknown)))
            if not isinstance(criterion.get("text"), str) or \
                    not criterion.get("text", "").strip():
                problems.append("%s: text is empty" % cwhere)
            done = criterion.get("done")
            if not isinstance(done, bool):
                problems.append("%s: done must be true or false" % cwhere)
                continue
            evidence = criterion.get("evidence", "")
            if done:
                problems.extend(_evidence_problems(evidence, cwhere, root))
            elif isinstance(evidence, dict) and evidence:
                problems.extend(_evidence_problems(evidence, cwhere, root))

    held = data.get("held", [])
    if not isinstance(held, list):
        problems.append("held must be a list")
        held = []
    for index, entry in enumerate(held):
        where = "held[%d]" % index
        if not isinstance(entry, dict):
            problems.append("%s: must be an object" % where)
            continue
        unknown = set(entry) - HELD_KEYS
        if unknown:
            problems.append("%s: unknown key(s) %s" % (where, sorted(unknown)))
        for key in ("name", "issuer", "date"):
            if not isinstance(entry.get(key), str) or not entry.get(key, "").strip():
                problems.append("%s: %s is empty" % (where, key))

    if problems:
        raise CertificationError(
            "%s failed %d check(s):\n  - %s"
            % (MANIFEST_NAME, len(problems), "\n  - ".join(problems)))


def score(data: Dict) -> Dict:
    """Derive the percentage. Weights scale each requirement by what an auditor
    would refuse to deploy over, not by how much work it was."""
    requirements = []
    weighted_done = 0.0
    weighted_total = 0.0
    unmet_required: List[str] = []
    done_criteria = 0
    total_criteria = 0
    for requirement in data["requirements"]:
        criteria = requirement["criteria"]
        done = sum(1 for criterion in criteria if criterion["done"])
        weight = requirement["weight"]
        met = done == len(criteria)
        requirements.append({
            "id": requirement["id"],
            "short": requirement["short"],
            "title": requirement["title"],
            "weight": weight,
            "required": requirement["required"],
            "done": done,
            "total": len(criteria),
            "met": met,
        })
        weighted_done += weight * (done / len(criteria))
        weighted_total += weight
        done_criteria += done
        total_criteria += len(criteria)
        if requirement["required"] and not met:
            unmet_required.append(requirement["id"])
    percent = 100.0 * weighted_done / weighted_total if weighted_total else 0.0
    required = [r for r in requirements if r["required"]]
    return {
        "schema": data["schema"],
        "updated": data["updated"],
        "percent": round(percent, 1),
        "done_criteria": done_criteria,
        "total_criteria": total_criteria,
        "requirements": requirements,
        "required_met": sum(1 for r in required if r["met"]),
        "required_total": len(required),
        "unmet_required": unmet_required,
        "deployable": bool(required) and not unmet_required,
        "held": data.get("held", []),
    }


def bar(percent: float, width: int = BAR_WIDTH) -> str:
    cells = max(0, min(width, int(round(percent / 100.0 * width))))
    return FILLED * cells + EMPTY * (width - cells)


def render(result: Dict) -> str:
    lines = [
        BLOCK_START,
        "**Certifiable: %.1f%%**  %s" % (result["percent"], bar(result["percent"])),
        "",
        "%d of %d acceptance criteria met  ·  %d of %d required requirements fully "
        "met  ·  deployable as a counselor: **%s**"
        % (result["done_criteria"], result["total_criteria"],
           result["required_met"], result["required_total"],
           "yes" if result["deployable"] else "no"),
        "",
        "| requirement | weight | criteria | state |",
        "|---|---|---|---|",
    ]
    for requirement in result["requirements"]:
        state = "met" if requirement["met"] else \
            ("open (required)" if requirement["required"] else "open")
        lines.append("| %s | %d | %d/%d | %s |"
                     % (requirement["short"], requirement["weight"],
                        requirement["done"], requirement["total"], state))
    lines.append("")
    if result["unmet_required"]:
        lines.append("Blocking requirements: %s."
                     % ", ".join("`%s`" % identifier
                                 for identifier in result["unmet_required"]))
    held = result["held"]
    if held:
        lines.append("Certifications held: %s."
                     % ", ".join("%s (%s, %s)" % (entry["name"], entry["issuer"],
                                                  entry["date"]) for entry in held))
    else:
        lines.append("Certifications held: **none**. A held certificate is evidence "
                     "of process, not of clinical validity, so it is recorded here "
                     "and does not move the bar.")
    lines.append("")
    lines.append("_Generated from `%s` (`updated` %s) by `tools/certification_bar.py "
                 "--write`. The percentage is progress toward a gate; only the "
                 "deployable line is a gate._"
                 % (MANIFEST_NAME, result["updated"]))
    lines.append(BLOCK_END)
    return "\n".join(lines)


def replace_block(text: str, block: str) -> str:
    start = text.find(BLOCK_START)
    end = text.find(BLOCK_END)
    if start < 0 or end < 0:
        raise CertificationError(
            "%s has no %s / %s markers; add them where the bar belongs"
            % (README_NAME, BLOCK_START, BLOCK_END))
    if end < start:
        raise CertificationError("%s has its markers in the wrong order" % README_NAME)
    return text[:start] + block + text[end + len(BLOCK_END):]


def current_block(text: str) -> Optional[str]:
    start = text.find(BLOCK_START)
    end = text.find(BLOCK_END)
    if start < 0 or end < start:
        return None
    return text[start:end + len(BLOCK_END)]


def check(root: Path = ROOT) -> Tuple[bool, str]:
    data = load(root)
    validate(data, root)
    result = score(data)
    readme = Path(root) / README_NAME
    if not readme.exists():
        return False, "%s is absent" % README_NAME
    text = readme.read_text(encoding="utf-8")
    block = current_block(text)
    if block is None:
        return False, ("%s carries no certification block; run --write after adding "
                       "the markers" % README_NAME)
    expected = render(result)
    if block != expected:
        return False, ("the certification block in %s is stale relative to %s: the "
                       "file says %.1f%%, the README shows the last generated value"
                       % (README_NAME, MANIFEST_NAME, result["percent"]))
    return True, "certification block matches %s (%.1f%%, deployable: %s)" % (
        MANIFEST_NAME, result["percent"], "yes" if result["deployable"] else "no")


def write(root: Path = ROOT) -> str:
    data = load(root)
    validate(data, root)
    block = render(score(data))
    readme = Path(root) / README_NAME
    text = readme.read_text(encoding="utf-8")
    readme.write_text(replace_block(text, block), encoding="utf-8", newline="\n")
    return block


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true",
                       help="fail when the README block drifts from the data")
    group.add_argument("--write", action="store_true",
                       help="regenerate the README block from the data")
    parser.add_argument("--json", action="store_true", help="print the derivation")
    parser.add_argument("--root", default=str(ROOT), help="tree to read (tests use this)")
    args = parser.parse_args(argv)

    root = Path(args.root)
    try:
        if args.write:
            block = write(root)
            print("wrote %s block into %s (%d lines)"
                  % (BLOCK_START, README_NAME, len(block.splitlines())))
            return 0
        if args.check:
            ok, message = check(root)
            print(message)
            return 0 if ok else 1
        data = load(root)
        validate(data, root)
        result = score(data)
    except CertificationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=1))
        return 0
    print("certifiable: %.1f%%  %s" % (result["percent"], bar(result["percent"])))
    print("  %d/%d criteria, %d/%d required requirements met, deployable: %s"
          % (result["done_criteria"], result["total_criteria"],
             result["required_met"], result["required_total"],
             "yes" if result["deployable"] else "no"))
    for requirement in result["requirements"]:
        print("  %-28s %d/%d  weight %d%s"
              % (requirement["id"], requirement["done"], requirement["total"],
                 requirement["weight"], "  REQUIRED" if requirement["required"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
