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
- audio mode (`native_dialogue` by default; otherwise `voiceover`, `dubbed_dialogue`, or explicitly requested `silent`), speakers, ambience and music plan;
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

The total duration equals the final section end time. Each Flow-bound section fits a supported generation duration or declares how it will be split. Apply the natural-Vietnamese review in `prompt-engineering.md` before approval and record the method and specific revisions in the checkpoint. Preserve approved dialogue verbatim in the corresponding scene prompts.

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
├── reference_images.json
├── references/images/          # actual approved image files
└── prompts/
    ├── scene_01.md
    └── ...
```

### `README.md`

Must state:

- model and aspect ratio;
- default clip duration and Extend policy;
- selected audio mode, defaulting to audible Vietnamese dialogue generated in Flow; do not assume a silent-output toggle exists;
- exact paste/generation order;
- character/reference reuse strategy;
- continuity and post-production text rules.

### `characters.md`

One stable block per recurring character:

- age range and cultural identity when relevant;
- face, hair, eyes and distinguishing stable features;
- fixed clothing, accessories and props;
- personality and performance range;
- voice/accent direction and approved image asset IDs;
- an explicit preservation sentence;
- shared negative constraints.

Do not include real customer identities or biometric reference material without explicit authorization.

### `master_prompt_sheet.md`

Use this table contract:

```text
scene_id | duration | aspect | model | audio_mode | prompt | ingredients | extend-to
```

Every generated scene appears exactly once. `prompt` may link to the full scene file while retaining a one-sentence production summary.

### `prompts/scene_<id>.md`

Each file contains:

- scene title;
- length, aspect, model, audio mode, approved image asset IDs and Extend plan;
- one complete English prompt in a fenced block;
- exact approved Vietnamese dialogue, speaker labels, delivery and turn order for native dialogue;
- audio direction matching the selected mode; request silence only for explicitly selected silent output;
- post-production overlay text outside the generation prompt.

### `clip_intake.md`

Must define:

- exact destination directory;
- deterministic `scene_<id>.mp4` names;
- alternate naming such as `_alt01`;
- visual and technical acceptance checks: identity against approved images, speech against the script, natural delivery/reactions, turn-taking and lip-sync; a validated prompt alone does not establish clip quality;
- the exact message that resumes the editing pipeline.

### `checkpoint.json`

Record a custom handoff exit without pretending it is a canonical generation stage:

```json
{
  "version": "1.1",
  "exit": "flow_handoff",
  "status": "completed",
  "mode": "spec-only",
  "generation_api_calls": 0,
  "cost_usd": 0,
  "scene_count": 0,
  "aspect_ratio": "9:16",
  "audio_mode": "native_dialogue",
  "scene_audio_modes": {},
  "dialogue_review": {
    "status": "reviewed",
    "method": "text_readthrough",
    "notes": "Record actual checks and revisions; replace this example."
  },
  "files": []
}
```

Populate `scene_count` and `files` with the actual output.
Use `scene_audio_modes` for overrides from the approved script, such as an expert voiceover scene; otherwise scenes inherit `audio_mode`. Include a `Dialogue:` section with exact speaker-tagged lines in every non-silent scene prompt.

### `reference_images.json`

Use `assets/templates/reference_images.template.json`. Include an `assets` array and a `scene_refs` object mapping every scene ID to its image asset IDs. Each asset requires:

```text
asset_id, role (character/environment/prop/keyframe/style), path, sha256
approval: status (approved), source (explicit user approval reference), approved_at (ISO 8601 with timezone)
```

Store actual images under `references/images/` using relative paths. Include at least the recurring characters and environments, plus any required props/keyframes. Each scene's Ingredients field must list its mapped asset IDs. Show the image set for approval before completing the handoff or generating video. Text-only approval does not approve unseen images. A changed image hash invalidates approval: request review of that version, never silently refresh the approval record. The validator checks files, hashes, mappings and recorded approval; it cannot authenticate user approval or judge visual suitability.

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
