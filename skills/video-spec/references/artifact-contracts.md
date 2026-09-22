# Artifact contracts

Use this reference while creating or reviewing the specification artifacts and final Google Flow bundle.

## Brief

The brief is complete when it records:

- title and one-sentence lesson;
- evidence summary: raw count, reviewed count, support rates and caveats;
- audience, channel, language, duration and aspect ratio;
- explicit scope and exclusions;
- wrong → teach → right structure or the user's chosen alternative;
- recurring cast and required layout;
- narration/dialogue, ambience and music plan;
- generation boundary and estimated cost.

## Script

The script contains ordered sections with stable IDs. Each section has:

```text
id
label
start_seconds / end_seconds
speaker and exact dialogue
performance direction
pace, emphasis and pause
post-production cue
evidence/source reference
```

The total duration equals the final section end time. Each Flow-bound section fits a supported generation duration or declares how it will be split.

## Scene plan

Each scene maps to a script section and contains:

```text
scene_id and type
start_seconds / end_seconds
description and shot intent
framing and movement
shot size, lens, lighting, depth of field and color temperature
character actions, emotion and dialogue reference
transition in/out
required character/environment/reference assets
post-only overlay notes
negative constraints
extend or split plan
```

The full scene plan also defines character continuity, palette by story phase, aspect ratio, text-safe areas and output audio policy.

## Flow handoff bundle

The final directory is:

```text
flow_handoff/
├── README.md
├── characters.md
├── master_prompt_sheet.md
├── clip_intake.md
├── checkpoint.json
└── prompts/
    ├── scene_01.md
    └── ...
```

### `README.md`

Must state:

- model and aspect ratio;
- default clip duration and Extend policy;
- **Return silent videos ON** when dubbing later;
- exact paste/generation order;
- character/reference reuse strategy;
- continuity and post-production text rules.

### `characters.md`

One stable block per recurring character:

- age range and cultural identity when relevant;
- face, hair, eyes and distinguishing stable features;
- fixed clothing, accessories and props;
- personality and performance range;
- voice reference if dialogue is being acted;
- an explicit preservation sentence;
- shared negative constraints.

Do not include real customer identities or biometric reference material without explicit authorization.

### `master_prompt_sheet.md`

Use this table contract:

```text
scene_id | duration | aspect | model | prompt | ingredients | extend-to
```

Every generated scene appears exactly once. `prompt` may link to the full scene file while retaining a one-sentence production summary.

### `prompts/scene_<id>.md`

Each file contains:

- scene title;
- length, aspect, model, ingredients and Extend plan;
- one complete English prompt in a fenced block;
- exact Vietnamese dialogue inside the prompt as a silent acting reference;
- a `Return silent video` instruction when applicable;
- post-production overlay text outside the generation prompt.

### `clip_intake.md`

Must define:

- exact destination directory;
- deterministic `scene_<id>.mp4` names;
- alternate naming such as `_alt01`;
- visual and technical acceptance checks;
- the exact message that resumes the editing pipeline.

### `checkpoint.json`

Record a custom handoff exit without pretending it is a canonical generation stage:

```json
{
  "version": "1.0",
  "exit": "flow_handoff",
  "status": "completed",
  "mode": "spec-only",
  "generation_api_calls": 0,
  "cost_usd": 0,
  "scene_count": 0,
  "aspect_ratio": "9:16",
  "return_silent_videos": true,
  "files": []
}
```

Populate `scene_count` and `files` with the actual output.

## Approval record

Record script and scene-plan approval in the host workflow's canonical checkpoint or decision log. If no checkpoint system exists, create a local decision record containing artifact version, status, approval source and timestamp. Never infer approval from silence.

## Privacy check

Before publishing or pushing artifacts, scan for:

- phone numbers, emails and addresses;
- customer or agent full names;
- raw call IDs when public disclosure was not authorized;
- transcript dumps;
- API keys, cookies and tokens;
- internal hostnames or database credentials.

Aggregate counts and anonymized behavior examples are the default public form.
