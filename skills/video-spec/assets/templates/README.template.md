# {{PROJECT_TITLE}} — Google Flow handoff

## Flow settings

- Model: **{{MODEL}}**
- Aspect ratio: **{{ASPECT_RATIO}}**
- Default length: **{{DEFAULT_DURATION}} seconds**
- Audio mode: **{{AUDIO_MODE}}** (default: native Vietnamese dialogue in Flow)
- Audio direction: {{AUDIO_DIRECTION}}
- Add subtitles, labels, logos and numeric claims in post-production.

## Paste order

1. Verify the actual character/environment images in `reference_images.json` were approved for their current hashes. Stop before video generation if approval is missing. Upload those exact images.
2. Attach the approved asset IDs listed in each scene's Ingredients field. Approve any new reference frame before adopting it.
3. Generate scenes in this order: {{GENERATION_ORDER}}.
4. Download every approved clip immediately and follow `clip_intake.md`.

## Continuity

{{CONTINUITY_RULES}}

## Dialogue review

{{DIALOGUE_REVIEW_NOTES}}

## Post-production overlays

{{OVERLAY_LIST}}
