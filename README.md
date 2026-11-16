# nurse-ratchet

Project Nurse Ratchet — the behavioural package of the AZAZAEL tree: one person's state, modelled and verified.

[![CI](https://github.com/myzticalbabe/nurse-ratchet/actions/workflows/ci.yml/badge.svg)](https://github.com/myzticalbabe/nurse-ratchet/actions/workflows/ci.yml)
[![Pages Deploy](https://github.com/myzticalbabe/nurse-ratchet/actions/workflows/pages-deploy.yml/badge.svg)](https://github.com/myzticalbabe/nurse-ratchet/actions/workflows/pages-deploy.yml)
[![License: SOUL FORGE](https://img.shields.io/badge/License-SOUL_FORGE-violet.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/myzticalbabe/nurse-ratchet)](https://github.com/myzticalbabe/nurse-ratchet/releases)
[![GitHub stars](https://img.shields.io/github/stars/myzticalbabe/nurse-ratchet?style=social)](https://github.com/myzticalbabe/nurse-ratchet/stargazers)

---

## Overview

Person state modelling and verification.

## Installation

```bash
pip install -e .
```

<!-- CERTIFICATION:START -->
**Certifiable: 22.6%**  █████░░░░░░░░░░░░░░░

4 of 19 acceptance criteria met  ·  0 of 6 required requirements fully met  ·  deployable as a counselor: **no**

| requirement | weight | criteria | state |
|---|---|---|---|
| crisis router recall | 3 | 1/3 | open (required) |
| construct data | 2 | 1/4 | open (required) |
| human in the loop | 3 | 1/3 | open (required) |
| comparator trial | 2 | 0/3 | open (required) |
| regulatory | 2 | 0/3 | open (required) |
| scope of practice | 2 | 1/3 | open (required) |

Blocking requirements: `crisis_router_recall`, `construct_data_from_people`, `human_in_the_loop`, `comparator_evidence`, `regulatory_classification`, `scope_of_practice`.
Certifications held: **none**. A held certificate is evidence of process, not of clinical validity, so it is recorded here and does not move the bar.

_Generated from `certification.json` (`updated` 2026-11-01) by `tools/certification_bar.py --write`. The percentage is progress toward a gate; only the deployable line is a gate._
<!-- CERTIFICATION:END -->

## Usage

python -m nurse_ratchet --help

## Architecture

See [Domain Atlas](https://myzticalbabe.github.io) for interactive visualization.

## Learning, access and community

This project is set up to be usable by teachers, club leaders and
self-taught learners as well as by developers:

| Document | What it covers |
|---|---|
| [STEM.md](STEM.md) | What this project teaches, and how to run it with a class, club or troop |
| [ACCESSIBILITY.md](ACCESSIBILITY.md) | What is keyboard-accessible, what has been verified, and what has not |
| [SUPPORT.md](SUPPORT.md) | Where to ask, and what to include |
| [SECURITY.md](SECURITY.md) | How to report a vulnerability privately |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute, including a path for first-timers |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Expected behaviour in issues and discussions |

## License

This project is licensed under the **SOUL FORGE License v1.0** — see [LICENSE](LICENSE) for details.

> *"Code is crystallized intention. Tend the fire."*

## Related Repositories

| Repo | Description |
|------|-------------|
| [azazael](https://github.com/myzticalbabe/azazael) | Monorepo: worm registry, cluster system, agent harness |
| [EveUnleashed](https://github.com/myzticalbabe/EveUnleashed) | Gamora, Lucy, Jaeger, Berzerker AIO native on 3.16t |
| [eliza](https://github.com/myzticalbabe/eliza) | Companion runtime: shards, adopted trees |
| [codex-video-engine](https://github.com/myzticalbabe/codex-video-engine) | CODEX Studio desktop app + video engine |
| [ecosystem-orchestrator](https://github.com/myzticalbabe/ecosystem-orchestrator) | ML platform install/orchestration |
| [scribe](https://github.com/myzticalbabe/scribe) | Documentation generation |
| [persephone-sync](https://github.com/myzticalbabe/persephone-sync) | Cross-platform env sync |
| [hydra-mlcluster](https://github.com/myzticalbabe/hydra-mlcluster) | Adaptive ML cluster processing |
| [flaming-sword](https://github.com/myzticalbabe/flaming-sword) | Defensive instrument: sentinel, compliance, formal verification |
| [shardex](https://github.com/myzticalbabe/shardex) | Shard execution engine |
| [krampus](https://github.com/myzticalbabe/krampus) | Composition: MellifluousML, Madi, Gamora, Eve, Lilith |
| [azazael-core](https://github.com/myzticalbabe/azazael-core) | Installable, interpreter-agnostic repackaging |
| [grantforge](https://github.com/myzticalbabe/grantforge) | AI-native grant tooling |
| [madi](https://github.com/myzticalbabe/madi) | Browsing instrument: fetch, challenge taxonomy, scorer |
| [jaeger](https://github.com/myzticalbabe/jaeger) | Durable spans, JSONL ledger, stdlib only |
| [cradle](https://github.com/myzticalbabe/cradle) | Composition over FLAMING SWORD, REAPER, GRIMOIRE |
| [esquire-admissibility](https://github.com/myzticalbabe/esquire-admissibility) | AI-evidence admissibility gates |
| [nurse-ratchet](https://github.com/myzticalbabe/nurse-ratchet) | Behavioural package: person state modelled |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Links

- **Monorepo**: https://github.com/myzticalbabe/azazael
- **Landing Hub**: https://myzticalbabe.github.io
- **Domain Atlas**: https://myzticalbabe.github.io/index.html
- **Issues**: https://github.com/myzticalbabe/nurse-ratchet/issues
- **Discussions**: https://github.com/myzticalbabe/nurse-ratchet/discussions