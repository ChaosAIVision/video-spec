# Clip intake

Download approved clips to:

`{{ABSOLUTE_CLIP_DIRECTORY}}`

Use deterministic names:

```text
scene_01.mp4
scene_02.mp4
```

Name alternates `scene_01_alt01.mp4`, `scene_01_alt02.mp4`, and so on.

## Acceptance checks

- Compare faces, clothing, environment and props with the approved reference images.
- Check audible dialogue against the approved script: correct speaker, wording, meaning and pronunciation.
- Listen for natural Vietnamese phrasing, pace, pauses and plausible reactions; reject robotic reading or forced politeness.
- Check turn-taking, listener behavior and lip-sync; follow the chosen audio mode.
- Record the rejected clip and correction needed before regenerating.

{{ADDITIONAL_ACCEPTANCE_CHECKS}}

## Exact return-handoff message

```text
I downloaded all approved Google Flow clips to {{ABSOLUTE_CLIP_DIRECTORY}}.
Resume from the separately authorized asset-review stage, map every scene_id to its path,
register source_tool="google_flow" and subtype="generated", then continue only through
the stages I authorize.
```

