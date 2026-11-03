#!/usr/bin/env python3
# coding: utf-8
"""Gate: the certification bar must be derived, current, and refused when unearned.

The negative controls carry the value here, because a percentage is a claim and
the failure mode of a claim is silent:

* a criterion with `done: true` and no evidence must be REFUSED, or the bar is
  just another number typed by whoever last touched the file;
* an evidence path that does not exist must be refused by name, so the number
  cannot survive the file it was justified by;
* a misspelled key must be refused rather than defaulting to `done: false`, or a
  requirement can sit at 0% for a year because someone wrote `donee`;
* `deployable` must stay false while any required requirement is open, even at a
  high percentage -- that is the difference between progress and permission;
* a stale README block must fail its own check, because the alternative is a
  published number that no longer matches the data behind it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
# (bootstrap removed by publicize: the package is installed)
sys.path.insert(0, str(ROOT / "tools"))

import certification_bar as CB

START, END = CB.BLOCK_START, CB.BLOCK_END


def _criterion(done: bool = False, evidence="", text: str = "a criterion") -> dict:
    return {"text": text, "done": done, "evidence": evidence}


def _evidence(note: str = "shows it") -> dict:
    return {"path": "evidence.md", "note": note}


def _requirement(identifier: str, weight: int = 1, required: bool = True,
                 criteria=None) -> dict:
    return {"id": identifier, "title": identifier.replace("_", " ").title(),
            "short": identifier, "weight": weight, "required": required,
            "criteria": criteria if criteria is not None else [_criterion()]}


def _tree(tmp_path: Path, requirements, held=None, readme: str = None) -> dict:
    """A miniature project: one README with empty markers, one evidence file."""
    (tmp_path / "evidence.md").write_text("evidence\n", encoding="utf-8")
    if readme is None:
        readme = "# t\n\n%s\n%s\n\ntail\n" % (START, END)
    (tmp_path / "README.md").write_text(readme, encoding="utf-8")
    data = {"schema": CB.SCHEMA, "updated": "2026-11-01", "note": "n",
            "held": held if held is not None else [], "requirements": requirements}
    (tmp_path / "certification.json").write_text(json.dumps(data, indent=1),
                                                 encoding="utf-8")
    return data


# -- the percentage ---------------------------------------------------------

def test_percentage_is_weighted_over_criteria(tmp_path):
    _tree(tmp_path, [
        _requirement("heavy", weight=3, criteria=[_criterion(True, _evidence()),
                                                  _criterion()]),
        _requirement("light", weight=1, criteria=[_criterion(True, _evidence())]),
    ])
    data = CB.load(tmp_path)
    CB.validate(data, tmp_path)
    result = CB.score(data)
    # (3 * 0.5 + 1 * 1.0) / 4 == 62.5
    assert result["percent"] == 62.5
    assert result["done_criteria"] == 2 and result["total_criteria"] == 3


def test_everything_open_is_zero_and_not_deployable(tmp_path):
    _tree(tmp_path, [_requirement("only", weight=3)])
    data = CB.load(tmp_path)
    CB.validate(data, tmp_path)
    result = CB.score(data)
    assert result["percent"] == 0.0
    assert result["deployable"] is False
    assert result["required_met"] == 0 and result["required_total"] == 1


# -- refusals ---------------------------------------------------------------

def test_done_criterion_without_evidence_is_refused(tmp_path):
    _tree(tmp_path, [_requirement("r", criteria=[_criterion(True, "")])])
    data = CB.load(tmp_path)
    with pytest.raises(CB.CertificationError, match="evidence"):
        CB.validate(data, tmp_path)


def test_evidence_path_that_does_not_exist_is_named(tmp_path):
    _tree(tmp_path, [_requirement("r", criteria=[
        _criterion(True, {"path": "absent.md", "note": "n"})])])
    data = CB.load(tmp_path)
    with pytest.raises(CB.CertificationError, match="does not exist here: absent.md"):
        CB.validate(data, tmp_path)


def test_misspelled_key_is_refused_rather_than_read_as_false(tmp_path):
    criterion = _criterion()
    criterion["donee"] = True          # the typo that would read as "not done"
    _tree(tmp_path, [_requirement("r", criteria=[criterion])])
    data = CB.load(tmp_path)
    with pytest.raises(CB.CertificationError, match="unknown key"):
        CB.validate(data, tmp_path)


def test_requirement_without_criteria_is_refused(tmp_path):
    _tree(tmp_path, [_requirement("r", criteria=[])])
    data = CB.load(tmp_path)
    with pytest.raises(CB.CertificationError, match="non-empty list"):
        CB.validate(data, tmp_path)


def test_duplicate_requirement_ids_are_refused(tmp_path):
    _tree(tmp_path, [_requirement("same"), _requirement("same")])
    data = CB.load(tmp_path)
    with pytest.raises(CB.CertificationError, match="duplicate id"):
        CB.validate(data, tmp_path)


# -- the gate, which is not the percentage ----------------------------------

def test_deployable_is_a_gate_not_a_percentage(tmp_path):
    requirements = [
        _requirement("safety", weight=3, criteria=[_criterion(True, _evidence())]),
        _requirement("legal", weight=2, criteria=[_criterion(True, _evidence()),
                                                  _criterion()]),
    ]
    _tree(tmp_path, requirements)
    data = CB.load(tmp_path)
    CB.validate(data, tmp_path)
    result = CB.score(data)
    assert result["percent"] == 80.0          # (3 + 1.0) / 5
    assert result["deployable"] is False      # one required requirement is open

    requirements[1]["criteria"][1] = _criterion(True, _evidence())
    _tree(tmp_path, requirements)
    data = CB.load(tmp_path)
    CB.validate(data, tmp_path)
    assert CB.score(data)["deployable"] is True


# -- rendering and drift ----------------------------------------------------

def test_bar_has_a_fixed_width_and_saturates_at_the_ends():
    assert len(CB.bar(0)) == CB.BAR_WIDTH
    assert CB.bar(0) == CB.EMPTY * CB.BAR_WIDTH
    assert CB.bar(100) == CB.FILLED * CB.BAR_WIDTH
    assert CB.bar(50) == CB.FILLED * 10 + CB.EMPTY * 10
    assert CB.bar(-5) == CB.EMPTY * CB.BAR_WIDTH          # a bad input cannot overflow
    assert len(CB.bar(1000)) == CB.BAR_WIDTH


def test_write_then_check_round_trip_and_detected_drift(tmp_path):
    _tree(tmp_path, [_requirement("r", criteria=[_criterion(True, _evidence())])])
    CB.write(tmp_path)
    ok, message = CB.check(tmp_path)
    assert ok, message
    assert "100.0%" in message

    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    (tmp_path / "README.md").write_text(readme.replace("100.0%", "42.0%"),
                                        encoding="utf-8")
    ok, message = CB.check(tmp_path)
    assert not ok
    assert "stale" in message


def test_check_refuses_a_readme_without_markers(tmp_path):
    _tree(tmp_path, [_requirement("r")], readme="# t\nno markers here\n")
    ok, message = CB.check(tmp_path)
    assert not ok
    assert "markers" in message


def test_held_certificate_is_shown_and_does_not_move_the_number(tmp_path):
    requirements = [_requirement("r", criteria=[_criterion(True, _evidence()),
                                                _criterion()])]
    _tree(tmp_path, requirements)
    baseline = CB.score(CB.load(tmp_path))["percent"]

    _tree(tmp_path, requirements, held=[{"name": "SOC 2 Type II",
                                         "issuer": "an auditor",
                                         "date": "2026-10-01"}])
    data = CB.load(tmp_path)
    CB.validate(data, tmp_path)
    result = CB.score(data)
    assert result["percent"] == baseline      # process evidence is not clinical evidence
    assert "SOC 2 Type II" in CB.render(result)


def test_the_repository_bar_is_current():
    """The README a reader sees must match certification.json right now."""
    ok, message = CB.check(ROOT)
    assert ok, "%s -- run tools/certification_bar.py --write" % message
