---
name: video-spec
description: Turn QC evidence or an approved training topic into a video specification and Google Flow handoff. Use for scripting, scene planning, character continuity, receiving generated clips, or explicitly requested voice and video post-production; generation and composition require their own authorization.
---

# Video Spec

Produce a traceable specification before video generation. Preserve the user's scope, exclusions, language, cast, platform, and delivery format.

## Operating boundary

For a specification request, start in **spec-only mode**: analysis and local artifacts may proceed; generation calls, Flow credit spending, publishing, and messages to external systems require the user's explicit authorization for that action. A request to edit received clips authorizes the local post-production branch; read [references/postproduction.md](references/postproduction.md) and preserve the source media. If OpenMontage is available and the user requests it, use its pipeline, stage directors, schemas, and checkpoints rather than recreating them.

Keep private source material local. Public outputs contain aggregate findings and anonymized examples unless the user explicitly authorizes identifiable data.

## Workflow

Use these steps for specification requests. For an authorized edit of existing clips, go directly to [references/postproduction.md](references/postproduction.md); do not restart the brief, script and image-approval gates.

1. **Lock the brief.** Record audience, source scope, date window, exclusions, duration, aspect ratio, language, cast, visual layout, and requested deliverables. Resolve only choices that materially change the output.
2. **Verify the lesson.** Rank candidate errors after exclusions, inspect supporting transcripts and coaching advice, and choose a teachable behavior supported by observable evidence—not merely the largest raw count. Read [references/workflow.md](references/workflow.md) for the evidence protocol.
3. **Write the learning arc.** Use `wrong situation → formal explanation → corrected replay` unless the user chose another format. Show the same objection/context in wrong and right versions so the changed behavior is isolated.
4. **Gate the script.** Write conversational Vietnamese and run the natural-dialogue review in `references/prompt-engineering.md`. Record the review method and specific revisions; include acting directions, timing, and post-production overlays. Present it for approval and stop. Do not create the scene plan until approval is explicit.
5. **Plan the scenes.** Each generated clip has one dominant beat, a bounded duration, camera language, emotion transition, continuity assets, dialogue reference, post-only text, and negative constraints. Present the scene plan for approval and stop.
6. **Approve the reference images and build the handoff.** Prepare or collect actual character, environment and required key-prop images, present the images for user approval, and record approval for each exact image version in `reference_images.json`. A text description is not an approved image. Draft prompts may proceed, but do not mark the handoff ready or generate video while any required image is missing, rejected or awaiting approval. After approval, create every artifact defined in [references/artifact-contracts.md](references/artifact-contracts.md). Construct prompts using [references/prompt-engineering.md](references/prompt-engineering.md) and the templates under `assets/templates/`.
7. **Validate.** Run `python3 scripts/validate_bundle.py <flow_handoff_dir> --expected-scenes N`. Resolve every error before delivery.
8. **Choose Flow mode.** Manual paste is the default. Browser-driven operation requires an authenticated session; announce every credit-spending Generate action and wait for confirmation unless the user explicitly authorized automatic generation for the current run.
9. **Receive clips.** Require deterministic `scene_<id>.mp4` names and verify continuity and technical integrity. When the user requests editing or composition, follow [references/postproduction.md](references/postproduction.md) for voice consistency, cut decisions, transitions, music and release checks.

## Binding quality rules

- Distinguish **frequency** from **confidence**. Report both the raw count and the evidence/advice support rate.
- Exclusions apply before ranking. Never let an excluded opening, closing, compliance, or other module win by frequency.
- The lesson names one observable behavior and one actionable replacement.
- Titles and Vietnamese content use real UTF-8 characters, not escaped `\uXXXX` sequences or unaccented substitutions.
- Flow prompts are English for visual control; preserve approved Vietnamese dialogue verbatim as spoken dialogue. Default to `native_dialogue` in Flow. Use `voiceover`, `dubbed_dialogue`, or `silent` only when selected for the project; never force silence or assume a silent-output UI toggle exists.
- Generated clips contain clean picture: text, subtitles, labels, logos, and numeric claims are post-production overlays.
- Recurring characters have stable identity blocks. Dialogue layouts preserve the user's requested screen side across every relevant scene.
- Natural speech is a release criterion: short speakable turns, consistent forms of address, credible objections, and responses tied to the previous turn. Preserve the teaching behavior and factual meaning while rewriting. Do not invent a successful sale or unapproved product claims.
- Map every scene to approved image asset IDs and verify the actual files and hashes before generation. Changed reference images invalidate their approval and require review again.
- Specify speaker, exact line, delivery, turn order and listener behavior for native dialogue; check actual generated speech and lip-sync at clip intake. When dubbing, define the audio timing and lip-sync workflow rather than assuming silent acting will match later audio.
- Cap a single Flow generation at the selected model's supported length. Give longer beats an explicit Extend or split plan.
- A completed handoff contains no transcript dumps, customer identifiers, credentials, or provider secrets.

## Completion

A specification task is complete when the approved lesson is traceable to evidence; script, scene plan and actual reference-image approvals are recorded; the natural-dialogue review is documented; the Flow bundle passes the validator; cost/API usage is reported; and the user receives a precise next action. Structural validation does not certify natural delivery or audiovisual quality; inspect generated clips separately. An authorized post-production task is complete when the requested edit is verified on the rendered output and the exact deliverable and preserved source paths are reported.
