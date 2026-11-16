# STEM learning guide — nurse-ratchet

Nurse Ratchet models one person's state and verifies it: the behavioural package of the tree, with a certification bar that checks the repository's own claims.

This guide is for teachers, mentors, club leaders, parents and students who want to
use this repository as a vehicle for real STEM learning — in particular for girls and
other groups still under-represented in computing, engineering and mathematics. It
says what the project actually teaches, how to run a session with it, and what to
remove so that nobody is excluded by accident.

## What this project teaches

**Subject areas**

- behavioural modelling
- verification
- data ethics
- testing claims

**Skills practised**

- writing a claim that can be tested
- separating observation from interpretation
- deciding what must not be recorded

## Prerequisites

Python 3.10 or newer. No clinical background, and no real personal data is used anywhere in the exercises.

Nothing else is assumed for the entry-level activity below: no prior programming
experience, no particular hardware, and no home internet connection.

## Six practices this repository is set up to support

These follow the published guidance on gender-equitable STEM education — connect the
work to learners' lives, let them investigate real problems, treat struggle as part of
the work, name and challenge stereotypes, make the work collaborative, and put
learners in front of diverse role models.

1. **Connect it to their lives.** a fitness tracker's 'readiness score' — same arithmetic, same question about what it actually knows
2. **Let them investigate.** ask the group to find a claim in the README that the test suite does not actually check
3. **Make struggle normal.** Build the session so that the first attempt is *expected*
   to fail. Say out loud that debugging is the subject, not a penalty. Ask "what did
   that error tell you?" before offering the answer.
4. **Challenge the stereotype.** Name who does this work and why it is not a gendered
   skill. Praise the method ("you isolated the variable"), not the person ("you're a
   natural") — the second kind of praise teaches learners that ability is fixed.
5. **Make it social.** pairs write a claim and a test for it, then swap and try to break each other's test
6. **Show diverse role models.** clinical informaticists and the ethicists who set limits on behavioural data

## A 90-minute session

1. *(15 min)* List every claim the README makes.
2. *(25 min)* Match each claim to a test, and mark the gaps.
3. *(35 min)* Write the missing test, including what should fail.
4. *(15 min)* Discuss: which claims should not be made at all?

## Vocabulary to define before the session

Specialist vocabulary is a hidden entry test if nobody explains it. Define each of
these the first time it appears, in one sentence, in the learners' own words:

1. **claim** — a statement the repository makes about itself.
2. **certification bar** — the check that the claim is still true.
3. **proxy** — a measurable stand-in for something unmeasurable.

## Accessibility

Read [ACCESSIBILITY.md](ACCESSIBILITY.md) before running a session. Two rules matter
most in a mixed-ability room:

- Every activity must be completable with a keyboard alone, with a visible focus ring.
- Every instruction names the control or the heading ("the **Run** button in the
  toolbar"), never a colour or a position.

Pair learners rather than singling anyone out, and always offer a text-only route for
a visual step.

## Contributing as a learner

Small, well-scoped contributions are the point, not a consolation prize:

- Browse issues labelled
  [`good first issue`](https://github.com/myzticalbabe/nurse-ratchet/labels/good%20first%20issue).
- Read [CONTRIBUTING.md](CONTRIBUTING.md) — it has a section written for first-time
  contributors.
- Ask in [SUPPORT.md](SUPPORT.md) if anything is unclear. Asking is expected here; it
  is not a failure.

## Licence and classroom reuse

Classroom, club and workshop use is welcome. See `LICENSE` for the exact terms, and
check whether your institution requires a separate agreement before redistributing
modified copies.
