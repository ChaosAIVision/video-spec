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

{{ACCEPTANCE_CHECKS}}

## Exact return-handoff message

```text
I downloaded all approved Google Flow clips to {{ABSOLUTE_CLIP_DIRECTORY}}.
Resume from the separately authorized asset-review stage, map every scene_id to its path,
register source_tool="google_flow" and subtype="generated", then continue only through
the stages I authorize.
```
