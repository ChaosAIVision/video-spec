# video-spec

Codex skill for turning QC error data and transcripts into an evidence-backed training-video specification and a paste-ready Google Flow handoff.

The workflow is designed around a clear learning contrast:

```text
wrong situation → expert explanation → corrected situation
```

It separates raw error frequency from transcript evidence, preserves Vietnamese dialogue and accents, requires approval of actual reference images, reviews natural Vietnamese dialogue, and validates the final Flow bundle before generation. Audible Vietnamese dialogue in Flow is the default; silent output is optional only when requested.

## Install

Copy or symlink the skill folder into your Codex skills directory:

```bash
cp -R skills/video-spec ~/.codex/skills/video-spec
```

Then invoke it with `$video-spec`, or describe a request involving QC insights, training-video scripting, scene planning, or Google Flow handoff creation.

## Repository structure

```text
skills/video-spec/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── assets/templates/
└── scripts/validate_bundle.py
tests/
└── test_validate_bundle.py
```

## Validate

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/video-spec
python3 -m unittest discover -s tests -v
python3 skills/video-spec/scripts/validate_bundle.py /path/to/flow_handoff --expected-scenes 10
```

The repository intentionally contains no call IDs, customer data, transcript dumps, API keys, or provider credentials.

