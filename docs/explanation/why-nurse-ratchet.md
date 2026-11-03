# Why Project Nurse Ratchet is built this way

Explanation, not instruction. If you want the surface, read
[`../reference/psyche.md`](../reference/psyche.md).

## The problem with a therapeutic agent is trust, not capability

Weizenbaum wrote ELIZA as a joke about therapy and found that people disclosed to
it anyway, and Nurse Ratched was written as an antagonist whose manner is
difficult to separate from care. Sixty years later the lesson has not changed shape: a system that
responds in the register of a listener will be believed in proportion to how well
it sounds, and nothing about that belief tracks whether anything underneath is
doing the work. A language model makes this worse by making the sound nearly free.

So the build question is not "can it respond usefully". It is: **what structure
would make it possible to tell whether it is working, and to stop it when it is
not?** Every decision below follows from that, and most of them cost capability.

## Four layers, because each one has to be measurable alone

`traits` and `affect` give a description: six domains and a PAD state with OCC
appraisal. That is necessary and it is not a mechanism — it says where someone
sits, never how a state moves. So `network.py` adds movement: constructs as nodes,
conditional dependence as edges. That framing comes from network psychometrics
(Borsboom et al. 2021), where the disorder is the dense self-sustaining core of
the graph rather than a latent quantity behind the symptoms. It was chosen because
it is *inspectable*: a person can be shown their own edges and disagree with one.

Then a graph is slow. `intuition.py` compiles it. The mechanism is not
Kahneman's "System 1", which is a description of two modes; it is recognition-
primed decision making (Klein), which is a claim about what recognition *is* —
compiled inference, with the slow evaluation retained as the source of truth. That
retention is what makes the fast path gradeable: `agreement()` reports whether the
compiled answer still matches the deliberate one, and `calibration()` reports a
Brier score with the count it rests on.

Finally `rt_agent.py` spends what the first three produced. Here the JITAI
literature (Nahum-Shani et al. 2018) is decisive on a point that is easy to skip:
*timing is part of the intervention*. A skills exercise delivered at arousal 0.9 is
not a neutral mistake — it teaches the person that the exercise does not work. So
the loop has a receptivity gate and a `regulate` stance that pre-empts skill work,
and `LEARNING_WINDOW_AROUSAL` is annotated in the source as clinical convention
rather than something measured here, because it is.

## Three decisions that cost capability on purpose

**The safety branch cannot be scored.** Triage runs before any stance utility is
computed, and a crisis verdict ends the turn. The first version damped other
stances by 0.15; that let a change-work stance win 0.75 to 0.67, and a test caught
it. A safety check that can be outbid is a safety check in name only.

**A wrong intuition is never corrected in place.** `resolve()` marks a prototype
wrong and leaves its profile alone. The tempting alternative — nudge the profile
toward the truth — destroys the evidence: after an update, the same error can no
longer be made, so the error rate can never be measured. Keeping the mistake costs
accuracy and buys the only honest number in the module.

**Nothing is inferred from text that should be measured.** `psyche_fit_pams.py`
refuses to build a graph from `tags` co-occurrence or from keywords in memory
content. Both would produce a graph-shaped artefact with real numbers in it that
answers a different question, and this project has already paid for that mistake
in another form.

## What the measurements changed

Decisions above were made first; these were made *because a number disagreed*.

| what was believed | what was measured | what changed |
|---|---|---|
| cosine similarity over the union is a fine matcher | an exact 2-of-4 instance scored 0.76, so the 0.62 threshold could never be reached and the fast path fired 0 times in 100 calls | match on measured coordinates, discount by `sqrt(coverage)` |
| that fix is enough | sparse cues then became unreachable at *any* support | coverage ladder: recognised, then trusted only with coverage; regression test added |
| a 0.15 penalty caps the dose under elevated risk | `reframe` still won, 0.75 vs 0.67 | cap the candidate set to low-dose stances |
| an exact-phrase crisis list is adequate | recall 0.76, all three misses euphemisms | paraphrase patterns + attribution guard |
| four patterns fixed it | dev 1.00, **holdout 0.33** | nothing — the holdout was not burned; the gap is published instead |
| concept families replaced patterns | holdout2 **0.83**, holdout3 **0.18** | the single number does not exist yet; the spread is published instead of the mean |

That last row is the most important thing in this repository. The improvement
looked complete on the data it was built from. The holdout split is the only
reason anyone can see that it is not, and the discipline that follows is blunt:
if you need new data to fix a miss, write a new holdout and say so.

## The unsolved tension

There are two readings of this stack and they are in genuine conflict.

The **therapeutic** reading wants the person to change: recognise the pattern, edit
the edge, watch the state move. A visible graph is a mirror, and mirrors work.

The **epistemic** reading notices that the same visibility is a feedback loop. If a
person learns what their prototypes are and adapts toward the reading, the
instruments that measure them are measuring their adaptation to the instruments.
Calibration numbers become a property of the measurement apparatus.

Nothing in this release resolves that. `IntuitionIndex` keeps its resolution ledger
precisely so the loop is at least *detectable* — a distribution of resolutions that
drifts toward the system's own predictions is visible in the ledger — but
detection is not mitigation, and calling it mitigation would be exactly the kind of
confident claim this project exists to avoid.

## Why publish at all, and why not everything

The method is general: flocks, tiered evidence, negative universes, partial
correlation networks, evaluation splits. Anyone with their own data can run all of
it, which is the point. The case is not general — it is somebody's life, in
mental-health and tenancy records, and publishing it would be indefensible whatever
the licence said. So the instruments ship, the records do not, and
`PUBLIC_MANIFEST.json` plus a gate makes that a fact about the build rather than a
promise in a document.

## Why the numbers are quoted with their command

Every figure in this documentation names the command that produces it. That rule
exists because the alternative is a repository that accumulates digits nobody can
re-derive — and the first thing a reader should be able to do with any number here
is try to falsify it.
