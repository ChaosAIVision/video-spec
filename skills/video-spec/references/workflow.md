# Evidence-to-video workflow

Use this reference when the input includes error tables, call IDs, transcripts, coaching advice, agent cohorts, source filters, or module exclusions.

## 1. Lock the analysis frame

Write a compact scope before querying or ranking:

| Field | Required decision |
|---|---|
| Population | brand, channel/source, agent cohort and seniority rule |
| Time | reference date and call/report date range |
| Exclusions | modules, dispositions, test calls, invalid rows |
| Unit | unique call, evaluation row, agent-call pair, or another explicit unit |
| Output | training lesson, call list, agent list, charts, or video spec |

Apply exclusions before aggregation. Deduplicate using the selected unit before counting.

## 2. Build the evidence table

For every candidate error, capture:

- raw occurrence count;
- number of unique calls and agents;
- source/channel distribution;
- transcript evidence available count;
- transcript evidence that visibly supports the error;
- coaching/advice rows that recommend the same correction;
- contradictory or `NO DATA` rows;
- representative anonymized excerpts or internal references.

Calculate at least:

```text
evidence_support_rate = supported_transcripts / transcripts_reviewed
advice_consistency_rate = matching_advice / advice_rows_reviewed
```

Do not treat missing transcript evidence as proof of failure. Label raw frequency, evidence confidence, and advice consistency separately.

## 3. Select the teachable behavior

Prefer the highest-frequency candidate that also passes these checks:

1. The behavior is visible or audible in transcripts.
2. The corrective advice is consistent across most reviewed cases.
3. The behavior can be changed by the target audience.
4. A wrong and corrected version can share the same context.
5. The lesson fits one sentence.

If the raw leader fails, document why and select the strongest evidence-backed candidate. Never hide the difference between “most frequent row” and “best-supported training lesson.”

## 4. Derive the causal insight

Inspect the transcript sequence around the error, not only the scored label:

- What did the customer say immediately before it?
- What did the agent do next: pause, interrupt, rebut, reassure, question, or redirect?
- How did the customer's language or posture change afterward?
- Which missing behavior would plausibly change that reaction?

State the insight as:

```text
When [trigger], agents often [observable behavior], causing [customer response].
Replace it with [specific behavior sequence].
```

Avoid diagnosing intent or personality when only behavior is observable.

## 5. Design the learning contrast

The default arc uses the same customer objection twice:

1. **Wrong:** reproduce the common mistake without caricature.
2. **Consequence:** show the customer's immediate reaction.
3. **Teach:** expert names the error and provides a short sequence.
4. **Replay:** restart from the same objection.
5. **Right:** agent performs the replacement behavior.
6. **Result:** show a realistic improvement, not a miraculous sale.

Keep the expert formal, concise, and nonjudgmental. A useful replacement sequence contains observable actions such as pause, acknowledge, clarify, and respond.

## 6. Write and gate the script

Every section includes:

- timestamp and target duration;
- spoken line;
- speaker, pace, emphasis and pause;
- facial expression and body action;
- source/evidence reference;
- post-production overlay, if any.

Read dialogue aloud or estimate speaking time. Split crowded exchanges rather than forcing multiple turns into an eight-second clip. Present the script, record approval, and stop before scene planning.

## 7. Plan visual beats and gate again

Map each section to one or more clips. Every generated scene defines:

- subject, action and environment;
- framing, shot size, lens, movement, lighting, depth and grade;
- emotion at start and end;
- character identity and wardrobe dependencies;
- transition and continuity reference;
- dialogue acting reference;
- text reserved for post-production;
- negative constraints and duration/Extend plan.

Check the whole sequence for repeated framing and slideshow risk. Deliberate repetition is valid when it enables a direct wrong/right comparison. Present the plan, record approval, and stop before building prompts.

## 8. Build, validate and hand off

After approval, create the complete bundle contract, run the validator, and report zero-cost/spec-only status. Ask whether Flow should be manual or browser-driven. Generated clips return under deterministic scene filenames; edit and compose are a separate authorization boundary.
