#!/usr/bin/env python3
"""Validate a Google Flow handoff bundle produced by the video-spec skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "characters.md",
    "master_prompt_sheet.md",
    "clip_intake.md",
    "checkpoint.json",
)
UNICODE_ESCAPE = re.compile(r"\\u[0-9a-fA-F]{4}")
SCENE_FILE = re.compile(r"scene_(\d+)\.md$")
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\b(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[\"']?[A-Za-z0-9_./+-]{16,}", re.I),
)


def _read_text(path: Path, errors: list[str]) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{path.name}: is not valid UTF-8")
        return ""
    except OSError as exc:
        errors.append(f"{path.name}: cannot be read: {exc}")
        return ""
    if UNICODE_ESCAPE.search(text):
        errors.append(f"{path.name}: contains escaped Unicode; write real UTF-8 characters")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path.name}: may contain a credential or secret")
            break
    return text


def validate_bundle(bundle: Path, expected_scenes: int | None = None) -> list[str]:
    """Return human-readable validation errors; an empty list means valid."""
    errors: list[str] = []
    bundle = bundle.resolve()
    if not bundle.is_dir():
        return [f"Bundle directory does not exist: {bundle}"]

    texts: dict[str, str] = {}
    for name in REQUIRED_FILES:
        path = bundle / name
        if not path.is_file():
            errors.append(f"Missing required file: {name}")
        else:
            texts[name] = _read_text(path, errors)

    prompt_dir = bundle / "prompts"
    if not prompt_dir.is_dir():
        errors.append("Missing required directory: prompts/")
        prompt_files: list[Path] = []
    else:
        prompt_files = sorted(prompt_dir.glob("scene_*.md"))

    scene_numbers: list[int] = []
    for path in prompt_files:
        match = SCENE_FILE.fullmatch(path.name)
        if match:
            scene_numbers.append(int(match.group(1)))
        else:
            errors.append(f"Invalid scene prompt filename: {path.name}")

        text = _read_text(path, errors)
        normalized = text.lower()
        if "return silent video" not in normalized:
            errors.append(f"{path.name}: missing 'Return silent video' instruction")
        if "Post only:" not in text:
            errors.append(f"{path.name}: missing post-production overlay line")
        if not re.search(r"no generated [^.\n]{0,80}(?:text|words)", normalized):
            errors.append(f"{path.name}: missing generated-text guardrail")
        if not re.search(r"-\s*Length:\s*\*\*\d+", text):
            errors.append(f"{path.name}: missing numeric clip length")
        if not re.search(r"-\s*Aspect:\s*\*\*[^*]+\*\*", text):
            errors.append(f"{path.name}: missing aspect ratio")

    actual_count = len(prompt_files)
    if expected_scenes is not None and actual_count != expected_scenes:
        errors.append(
            f"Expected {expected_scenes} scene prompts, found {actual_count}"
        )
    if scene_numbers:
        expected_numbers = list(range(1, len(scene_numbers) + 1))
        if scene_numbers != expected_numbers:
            errors.append(
                "Scene prompts must be consecutively numbered from scene_01: "
                f"found {scene_numbers}"
            )

    readme = texts.get("README.md", "")
    if "return silent videos" not in readme.lower():
        errors.append("README.md: missing silent-video setting")

    characters = texts.get("characters.md", "")
    if "Preserve the exact same" not in characters:
        errors.append("characters.md: missing explicit identity-preservation rule")

    master = texts.get("master_prompt_sheet.md", "")
    for field in ("scene_id", "duration", "aspect", "model", "prompt", "ingredients", "extend-to"):
        if field not in master:
            errors.append(f"master_prompt_sheet.md: missing table field '{field}'")

    intake = texts.get("clip_intake.md", "")
    if "scene_01.mp4" not in intake:
        errors.append("clip_intake.md: missing deterministic scene filename")

    checkpoint_path = bundle / "checkpoint.json"
    checkpoint: dict[str, object] = {}
    if checkpoint_path.is_file():
        try:
            checkpoint = json.loads(texts.get("checkpoint.json", ""))
        except json.JSONDecodeError as exc:
            errors.append(f"checkpoint.json: invalid JSON: {exc}")

    if checkpoint:
        required_values = {
            "exit": "flow_handoff",
            "status": "completed",
            "generation_api_calls": 0,
        }
        for key, value in required_values.items():
            if checkpoint.get(key) != value:
                errors.append(f"checkpoint.json: {key!r} must equal {value!r}")
        if checkpoint.get("scene_count") != actual_count:
            errors.append(
                "checkpoint.json: scene_count must match the number of prompt files"
            )
        if checkpoint.get("return_silent_videos") is not True:
            errors.append("checkpoint.json: return_silent_videos must be true")
        files = checkpoint.get("files")
        if not isinstance(files, list):
            errors.append("checkpoint.json: files must be an array")
        else:
            expected_paths = {f"prompts/{path.name}" for path in prompt_files}
            listed = {str(item) for item in files}
            missing = sorted(expected_paths - listed)
            if missing:
                errors.append(
                    "checkpoint.json: files is missing prompt entries: "
                    + ", ".join(missing)
                )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Path to flow_handoff directory")
    parser.add_argument("--expected-scenes", type=int)
    args = parser.parse_args(argv)

    errors = validate_bundle(args.bundle, args.expected_scenes)
    if errors:
        print(f"INVALID: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID: {args.bundle.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
