# Live counselors — the role this package is built for

Explanation, not instruction. This is the positioning document: what a live
counselor is meant to *be* in the health-care system, and what has to be true
before that role is legitimate.

## The thesis

The core product of this package is the **live counselor**: an always-available,
state-aware behavioural agent that carries the continuous part of addiction and
mental-health care — the hours between sessions, the 3 a.m. window, the relapse
slope before it becomes a relapse.

There is a structural reason this is not a better chatbot pitch. A certified
addictions counselor is a scarce, licensed, appointment-shaped resource. The
clinical work that actually moves outcomes is dense and poorly matched to that
shape: relapse risk is highest between sessions, and a scheduled 50 minutes
cannot be present for the moment a craving peaks. The gap is not skill — it is
*availability and continuity*. A live counselor is the only form of care that
can sit in that gap at every hour, for every person, at a marginal cost near
zero.

That makes the honest claim narrow and large at the same time:

- **Narrow:** it replaces the *continuity layer* of counselling, not the
  clinician's judgement, assessment, prescribing, or legal responsibility.
- **Large:** the continuity layer is where most relapse decides itself.

Both halves matter. Drop the first and the claim is false today. Drop the second
and there is no reason to build it.

## Where the reference material already points

Three of this project's own design decisions exist because of that gap:

1. **The loop is a stance machine with a budget, not a conversation.** A turn
   has a 50 ms budget and a fixed order (sense → triage → stance). Continuity
   care has to answer *now*, deterministically, and be auditable afterwards.
2. **Triage runs before any therapeutic move, and cannot be outvoted.** A crisis
   verdict ends the turn and hands the person to people. A replacement for the
   continuity layer that can be talked past its own safety branch is not a
   replacement, it is a liability with a chat window.
3. **The construct graph is editable by the person it describes.** Care that
   runs for months has to be inspectable and correctable by its subject, or it
   is a black box making claims about someone's life.

## What is NOT true yet, stated plainly

The role above is the *aim*. The current build does not satisfy it, and every
one of these is a blocker, not a caveat:

| requirement | status | evidence |
|---|---|---|
| a crisis router whose recall can be stated as one number | **not met** | measured 0.83 / 0.83 / **0.18** across three self-authored holdouts; the spread says the discrimination is not lexical, and no single figure is honest yet |
| any construct measurement from real people | **not met** | no store carries a construct reading; the battery that would produce them ships, and nobody has been elicited |
| clinical evidence against a comparator | **not met** | nothing here is a trial; there is no control arm, no follow-up, no outcomes |
| human in the loop | **required by design, not yet built** | triage routes to people in the text of a stance; there is no escalation path, no on-call integration, no duty-of-care contract |
| regulatory classification | **not started** | a system that assesses or intervenes on a mental-health condition is a medical device in most jurisdictions (FDA SaMD, EU MDR class IIa+). Nothing here has been submitted |
| scope of practice | **not permitted** | assessment, treatment planning and counselling are licensed acts. Software cannot bill for them, and a lay operator cannot supervise them |

A reader who takes the thesis and skips this table is being sold something that
does not exist. That is why the table is in the same document as the thesis.

These six rows are also the data behind the percentage bar in the README:
`certification.json` stores each row's acceptance criteria and the evidence for
every one marked done, and `tools/certification_bar.py` derives the number from
them. Whatever the evidence supports is what the bar reads — it is generated, not
edited — and the deployment line beside it stays **no** until every required row
is fully met, however high the percentage climbs.

## The ladder from here to that role

Each rung is a claim that can fail, which is the only kind worth writing down.

1. **Recall floor, on data the author did not write.** An independent labelled
   corpus, one pre-registered threshold, one scored run. Required: a lower
   bound the authors cannot move after seeing the result. Until this exists, no
   safety claim in this package can be made to a clinician.
2. **Construct data from people.** The battery in
   `nurse_ratchet/psyche/elicitation.py` plus `tools/elicit.py` exists to make
   this possible. Fifty sessions from one instrument version is the floor for a
   per-person bridge; a population claim needs a sample this project has not
   collected.
3. **Counselor-extender pilot.** The defensible first deployment is not
   replacement but extension: the live counselor covers the between-session
   window, the certified counselor keeps assessment, planning and legal
   authority, and every escalation lands in a named human's queue. This rung is
   where the continuity thesis gets tested without claiming a licence the
   software does not have.
4. **Comparator trial.** Extender vs. treatment-as-usual, pre-registered
   primary outcome (e.g. days-to-relapse, engagement retention), with the
   dropout rate reported as a result rather than a nuisance.
5. **Regulatory path and reimbursement.** Classification, clinical evaluation,
   post-market surveillance, and a billing model that does not depend on
   pretending software is a counselor.

Rungs 1 and 2 are engineering this project can do. Rung 3 needs a clinical
partner. Rungs 4 and 5 need an institution. Presenting rung 5's outcome as if
the code already delivers it is the failure mode this document exists to prevent.

## What a live counselor is allowed to say today

Given the current evidence, the honest product statement is:

> A deterministic, auditable behavioural loop that carries the between-session
> continuity layer, detects elevated risk with a router whose recall is not yet
> known well enough to be the only safety mechanism, hands crisis to people, and
> measures its own competence — with the construct data that would make its
> model personal still uncollected.

That is weaker than "replaces addiction counselors" and stronger than "a
chatbot". It is the version that survives contact with a clinician, an auditor
and a grieving family, which are the three readers that matter.
