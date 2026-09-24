---
name: storiestelling
description: Create engaging situation-driven video stories, roleplays, short dramas, and training scripts from topics, QC errors, source material, or reference transcripts. Use when users request storytelling, hooks, emotional arcs, natural character dialogue, or a compelling scenario. Default to dramatized interaction and visible character change, not presenter monologues or narrated lectures. Pair with video-spec for an authorized production handoff.
---

# Storiestelling

Turn an idea or lesson into something that happens to characters. Preserve the requested skill name `storiestelling`.

## Story contract

- Build around one focal character, one concrete goal, one central obstacle, and one observable change. Supporting characters may participate; “one character” does not mean a solo performance.
- Make dialogue, action, reactions, and choices carry the story. Default to no presenter and no voiceover. Add them only when requested, keeping the dramatic scene primary.
- Borrow structural principles from references: emotional contrast, a setback with stakes, a motivated turning point, and a payoff. Do not copy the reference's host-led delivery, characters, wording, or promotional segment automatically.
- Keep conflict proportionate to the setting. A hesitant customer, an awkward pause, a misunderstood cost, or an almost-ended call can supply enough tension. Do not manufacture tragedy or humiliation.
- Show a changed behavior before a changed outcome. A sales technique cannot guarantee a sale; a clearer question, regained attention, or a confirmed next step can be the payoff.
- Preserve approved facts, lesson scope, character identities, and existing scenario details. Do not silently replace the user's modules or split them into unrelated lessons.

## Workflow

### 1. Extract a compact brief

Use supplied context first. Identify audience, intended feeling, setting, character goal, central obstacle, required teaching behavior, facts that must remain exact, and target duration. Default to natural Vietnamese and a 60–90 second draft if missing; label that duration as an assumption.

Ask only for missing information that prevents a meaningful draft. Use clearly marked placeholders for unavailable prices or offers. Never invent commercial facts to finish a scene. If a reference is inaccessible, state that and use any supplied transcript without pretending to have watched the video.

### 2. Find the dramatic engine

Write one sentence internally: “[Character] wants [goal], but [obstacle], so must change [behavior] before [credible consequence].”

Choose an opening that immediately exposes friction: a line that nearly ends the conversation, an unexpected reaction, a contradiction, or a choice with consequences. Pay off the exact question raised by the hook. Avoid “Hôm nay chúng ta sẽ học…” and generic promises of a secret formula.

If the user asks for ideas, give up to three distinct scenario premises. Otherwise select the strongest premise and complete the script without a mandatory idea-selection stop.

### 3. Build the emotional arc

Use these functions flexibly; do not force six separate shots or fixed percentages:

| Beat | Dramatic function | What the viewer sees or hears |
|---|---|---|
| Hook | Open a meaningful question | A specific line, action, or reaction with immediate stakes |
| Setup | Make the goal understandable | Only the context needed to care about the next choice |
| Setback | Make the old approach fail or stall | A credible consequence and the other character's response |
| Turn | Motivate a different choice | A clue, realization, clarification, or brief coaching exchange |
| Changed action | Demonstrate the new behavior | Concrete dialogue or action that addresses the same obstacle |
| Payoff | Resolve the opening question | Visible progress, an earned outcome, or an honest partial resolution |

For every beat, name the emotional state before and after. Cut beats that neither change the situation nor reveal necessary information. Connect beats through cause and effect rather than a list of unrelated examples.

Choose a continuous scene by default. Use a clearly signaled rewind or parallel wrong/right versions only when useful or requested. Keep the customer, objection, offer, and context equivalent in a comparison. Never switch to a friendlier customer or add a new discount just to make the corrected version succeed.

### 4. Write playable dialogue

- Give characters distinct goals and knowledge. Make each response react to the immediately preceding line.
- Use short, speakable turns, usually one or two sentences. Allow hesitation, listening, and pauses when they change the scene; avoid filler in every line.
- Use consistent Vietnamese forms of address. For telesales, use “em – anh/chị” or the established age-appropriate form; do not switch casually to “mình.”
- Show feelings through observable behavior: a hand pauses above the end-call button, the customer asks a follow-up question, or the consultant stops reading and listens. Avoid abstract directions such as “make it viral.”
- Do not make characters recite teaching rubrics or explain concepts they would not naturally discuss. A trainer may appear in a brief, believable coaching scene if needed, not deliver an inserted lecture.
- Do not force an immediate purchase or an unrealistically grateful customer. Show customer confirmation before treating an order as agreed.
- Keep production directions separate from spoken words. Mark fictional dialogue as illustrative when it is derived from evidence rather than quoted from a real call.

For sales-training scenarios, read [references/sales-example.md](references/sales-example.md). Treat its pattern as an example, not a mandatory plot for all subjects.

### 5. Deliver the requested level

For a script request, return:

1. A short title and one-sentence premise.
2. A script table: `Approx. time | Visible action / reaction | Speaker and exact dialogue | Emotional shift`.
3. One short takeaway, preferably earned by the ending; add an end-card only when useful.
4. Any unresolved factual placeholders, kept outside spoken dialogue.

Estimate duration from speaking pace plus pauses and actions; label timing approximate. Read the lines aloud mentally and shorten overcrowded sections. If the user requests dialogue only, return the dialogue only. Do not create a large production bundle for a simple writing request.

For production work, hand off the premise, complete dialogue, emotional beats, cast, continuity constraints, factual sources, and approval status to `video-spec`. Treat this story format as the user's chosen alternative to its default formal-explanation structure. Follow its actual image-approval and generation workflow when applicable. Do not claim a script draft is an approved scene plan or a finished video, and do not spend generation credits merely because a script was requested.

### 6. Review and revise before delivery

Check these concrete failure modes:

- **Lecture disguised as drama:** If removing a narrator makes the scene incomprehensible, rewrite the interaction.
- **Flat arc:** If every beat has the same emotional state, add a credible setback or consequential choice.
- **Unmotivated recovery:** If the solution appears without a clue or decision, repair the turning point.
- **Fake payoff:** If the character says the right phrase and magically wins, give the other character a believable response.
- **Too much content:** Keep one main change; retain user-required material and propose separate episodes only if needed.
- **Changed experiment:** In wrong/right replays, verify the correction addresses the original objection under the same conditions.
- **Factual drift:** Check quantities, totals, offer compatibility, shipping, and claim provenance. Never combine conflicting source examples into one offer.
- **Unfilmable pacing:** Ensure dialogue fits the intended duration and actions fit the selected format. Preserve continuous phone/headset use and speaker identity across cuts.

Revise failing parts rather than attaching a generic checklist to the user's script. Do not promise virality or guaranteed learning/sales outcomes.
