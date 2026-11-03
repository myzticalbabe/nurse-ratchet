# Hardware Requirements — Project Nurse Ratchet

## Reference Platform (Development & Validation)

This project was **developed and validated exclusively on:**

| Component | Specification |
|-----------|---------------|
| **CPU** | Intel Core Ultra 9 285H (16 cores, 22 threads) |
| **iGPU** | Intel Arc 140T (8 GB shared VRAM) |
| **RAM** | 32 GB LPDDR5x-8533 (dual channel) |
| **OS** | Windows 11 Pro 24H2 (build 26100) |
| **Python** | 3.14.7 (free-threaded) / 3.15.0rc3 (free-threaded) |

## Component Architecture

| Package | Contents | Role |
|---------|----------|------|
| `nurse_ratchet` | `__init__.py` | Package root |
| `nurse_ratchet.psyche` | 8 modules + data | Core therapeutic agent |
| `tools/` | `publicize.py`, `psyche_fit_pams.py`, `eliza_release_gate.py`, `triage_eval.py` | Build & validation |
| `tests/` | 14 test modules | Verification |

### PSYCHE Modules (The Therapeutic Engine)

| Module | Role | Key Feature |
|--------|------|-------------|
| `traits.py` | OCEAN + H (Big Five + Honesty-Humility) | 60 IPIP-style items, editable artifact |
| `affect.py` | Temperament & OCC emotion families | P/A/D weights, elicitation structure |
| `network.py` | PersonNetwork: constructs + dynamics | Threat/reward/avoidance appraisal |
| `intuition.py` | Prototype matching (RPD) | MIN_SUPPORT=2, MATCH_FLOOR=0.55 |
| `rt_agent.py` | TherapeuticLoop: turn-based interaction | StructuredTurnResponse |
| `rt_channel.py` | Live channel: newline JSON over stdio | Console script entry point |
| `constructions.py` | Personal construct theory (Kelly) | Bipolar constructs, repertory grid |
| `elicitation.py` | Conversational construct elicitation | Laddering, pyramid, triadic sort |

### Local Failure Ledger (Standalone)

The package includes `_ledger.py` — a **stdlib-only replacement** for the monorepo's `CORE.failure_ledger`. It writes `failure_ledger.jsonl` in the package directory. No external dependency required.

## CARPE DIEMIC CREATIVE LICENCE {CDCL}

> **Developers have a Carpe Diem Creative Licence {CDCL} to freely modify this code for their interests.**

### What You Can Modify Freely

- **Item bank** (`traits.py`): Add/remove/rephrase the 60 IPIP-style items
- **Temperament weights** (`affect.py`): P/A/D multipliers for your population
- **Construct vocabulary** (`network.py`): Threat/reward/avoidance → your appraisal domains
- **Matching thresholds** (`intuition.py`): MIN_SUPPORT, MATCH_FLOOR for your data density
- **Turn structure** (`rt_agent.py`): StructuredTurnResponse fields for your protocol
- **Elicitation methods** (`elicitation.py`): Laddering/pyramid/triadic for your interview style

### What Requires Calibration

| Component | Calibration Tool | Target |
|-----------|------------------|--------|
| Trait scoring | `tests/test_psyche_traits.py` | Synthetic respondents recover known levels |
| Construct matching | `tests/test_psyche_network.py` | Threat/reward dynamics produce expected appraisals |
| Prototype matching | `tests/test_psyche_intuition.py` | Known prototypes match at > 0.55 cosine |
| RT channel | `python -m nurse_ratchet.psyche.rt_channel --selftest` | 13/13 assertions pass |

Run `pytest tests/` — all 14 test modules should pass on your hardware.

### Generated vs Authored

- **Authored**: `src/PSYCHE/*.py` (source of truth)
- **Generated**: `nurse_ratchet/psyche/*.py` via `tools/publicize.py`
- **NEVER edit generated files** — they are overwritten by `publicize.py`
- **Fix the source**, then re-run: `python tools/publicize.py`

## Porting to Other Platforms

| Platform | Changes Needed |
|----------|----------------|
| Linux/macOS | None — stdlib only; `_ledger.py` uses `pathlib`, `threading`, `json` |
| Different Python | 3.10+ works; `dataclasses`, `typing` features used |
| No free-threading | Works; parallel test runs slower but correct |

## Supported Python Versions

| Version | Status | Notes |
|---------|--------|-------|
| 3.10+ | Compatible | `Fraction`, `dataclasses`, `Annotated` |
| 3.14t | Recommended | Free-threaded; test parallelism |
| 3.15t | Recommended | Current development target |

## License

Apache-2.0 — see `LICENSE` and `NOTICE`.

---

*Generated 2026-11-02. Your therapeutic frame will differ — that's the point of {CDCL}.*