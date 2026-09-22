# Google Flow prompt engineering

Use this reference during script review, reference-image approval and Flow prompt assembly.

## Prompt assembly order

Build every scene prompt in this order:

1. duration, aspect ratio and visual style;
2. continuity/reference instruction;
3. composition and fixed screen-side rules;
4. subject, environment and lighting;
5. ordered actions and emotion transition;
6. audio mode, speaker-tagged Vietnamese dialogue, delivery and turn order;
7. camera, lens, depth of field and grade;
8. narrative intent;
9. audio direction consistent with the selected mode and relevant negative constraints.

Translate scene-plan camera fields into direct visual language:

| Scene-plan field | Prompt phrase example |
|---|---|
| `medium_close` | `medium close-up` |
| `dolly_in` | `slow controlled dolly in` |
| `lens_mm: 50` | `50mm lens` |
| `depth_of_field: shallow` | `shallow depth of field` |
| `color_temperature: warm` | `warm natural grade` |

## Character continuity

Create one identity block per recurring character and reuse its exact name in every prompt. Lock stable traits; vary only performance state.

Stable traits include face, age, hairstyle, wardrobe, accessories and recurring prop. Performance traits include emotion, posture, eye line, pace and gesture. Never encode a temporary emotion as part of the permanent identity block.

Before video generation, obtain user approval of actual images for every recurring character, environment and required key prop. Record paths, SHA-256 hashes, approval source and timestamp in `reference_images.json`; map every scene to its asset IDs. Show the actual images: approval of a written description or script does not approve unseen images. Missing or changed images block generation until approved.

Reuse approved master images as stable anchors. A frame from a generated scene is a candidate reference, not an automatic replacement for the master; inspect it and record approval before adopting it. If a corrected replay must mirror the wrong version, use its approved establishing frame and specify which actions or reactions change.

## Dialogue and acting

Write visual-control prose in English. Default to `native_dialogue`: request audible Vietnamese speech synchronized with the visible speaker. Preserve approved lines verbatim, label each speaker, and specify accent when agreed, pace, pauses and turn order. Keep the listener silent during the other person's turn unless intentional overlap is scripted. Verify actual speech and lip-sync on generated clips; a prompt is not a guarantee.

| Audio mode | Prompt and handoff requirements |
|---|---|
| `native_dialogue` (default) | Spoken Vietnamese dialogue, named speakers and natural delivery; no silent-output or no-audio instruction. |
| `voiceover` | State the narrator and whether audio comes from Flow or post-production. On-screen characters do not mouth the narration. |
| `dubbed_dialogue` | Include acting dialogue, approved external audio/timing and a lip-sync/alignment plan. Do not assume silent acting will match later audio. |
| `silent` | Use only when explicitly requested; omit spoken lines and request silent output. |

Use actual supported model controls; do not assume a `Return silent videos ON` UI toggle exists.

One video may mix modes, for example native dialogue in the customer scenes and expert voiceover between them. Record the default in checkpoint `audio_mode` and any approved per-scene overrides in `scene_audio_modes` (scene ID to mode). Keep the master sheet and each scene prompt consistent with these choices.

Keep each scene to one dominant exchange. If two complete turns crowd the duration, split the scene. Allow reaction time inside the clip; the customer's reaction should occur during the agent's line when that causal relationship matters.

## Natural Vietnamese dialogue review

Write spoken Vietnamese, not report prose. Give each turn one intent and usually one or two short sentences; let speaking time determine the cut. Use `em – anh/chị` for the consultant when appropriate and keep customer pronouns consistent with their role and age. Avoid mechanical repetition of `dạ`, excessive politeness markers, forced filler, textbook explanations and translated English syntax. Do not force slang or an accent the user has not requested.

Make every reply respond to the preceding line. Let customers hesitate, ask back or remain unconvinced; correct agent behavior need not yield a sale. Keep expert speech professional but speakable. Preserve evidence, the learning objective and approved facts when rewriting. Do not present adapted dialogue as an exact transcript quotation.

Example with the same objection and corrective intent:

- Customer: “Chị thấy giá cao quá, để chị suy nghĩ thêm.”
- Stiff consultant: “Em xin ghi nhận ý kiến của chị về vấn đề giá thành sản phẩm. Chị có thể chia sẻ thêm nguyên nhân được không ạ?”
- Natural consultant: “Dạ, chị đang thấy cao so với loại chị dùng, hay so với số tiền chị định chi ạ?”

Before script approval, run a text readthrough or listen to an actual readthrough when available. Check meaning, conversational linkage, pronouns, speaking time including pauses, and whether the expert sounds like a person. Revise awkward lines and record checkpoint `dialogue_review` with `status: reviewed`, `method: text_readthrough` or `audio_readthrough`, and specific notes. Never label a text estimate as an audio test. The record is not an automatic naturalness score. Re-review and obtain script approval after material dialogue changes.

## Text and overlays

Flow generates clean picture. Put overlay text after the prompt under `Post only:`. Reserve negative space in the composition if later graphics need it.

Explicitly request:

```text
No generated text, no subtitles, no labels, no logos, no watermark.
```

This hard guardrail is necessary because generated text is visually unstable and cannot preserve Vietnamese typography reliably.

## Split-screen dialogue

When the user specifies character sides, repeat the invariant in every dialogue prompt:

```text
Agent is always LEFT. Customer is always RIGHT. Keep the center divider fixed. No camera-side swap.
```

Use matched eye lines toward the divider. Keep both faces readable when reaction is part of the lesson. Vary shot scale or movement only when it preserves the comparison.

## Emotional legibility

Prefer restrained micro-actions:

- presses lips together;
- releases shoulders;
- pauses typing;
- holds eye contact;
- pulls phone slightly away;
- gives a small nod.

Describe both the starting and ending emotional state. Avoid generic directions such as “looks emotional”; name the visible action that communicates it.

## Wrong/right contrast

Hold context constant and change the target behavior:

| Wrong version | Correct version |
|---|---|
| no pause | visible pause |
| fast, defensive delivery | slower, grounded delivery |
| rebuttal or solution first | acknowledgment first |
| customer tightens posture | customer gradually relaxes |
| cooler, higher-contrast grade | warmer, softer grade |

The corrected outcome should remain realistic: renewed engagement is enough; a sale is not required.

## Model and duration

Use the model selected by the user or available in Flow. Treat eight seconds as the safe default unless the current model supports another limit. For a longer beat, either:

- split at a natural reaction boundary; or
- generate the opening clip and declare a precise Extend action that starts from its final frame.

Do not hide duration overflow inside a long prompt.

## Negative constraints

End with only constraints relevant to likely failures:

```text
No subtitles, no generated text, no logos,
no watermark, no extra people, no identity drift, no wardrobe change,
no camera-side swap, no exaggerated acting.
```

Add scene-specific constraints—such as no smile, no typing, or no product pack—only when they protect the lesson.
