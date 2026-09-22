#!/usr/bin/env python3
"""Validate a Google Flow handoff bundle produced by the video-spec skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from datetime import datetime


REQUIRED_FILES = (
    "README.md",
    "characters.md",
    "master_prompt_sheet.md",
    "clip_intake.md",
    "checkpoint.json",
    "reference_images.json",
)
UNICODE_ESCAPE = re.compile(r"\\u[0-9a-fA-F]{4}")
SCENE_FILE = re.compile(r"scene_(\d+)\.md$")
PLACEHOLDER = re.compile(r"\{\{[^{}]+\}\}")
AUDIO_MODES = {"native_dialogue", "voiceover", "dubbed_dialogue", "silent"}
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
    if PLACEHOLDER.search(text):
        errors.append(f"{path.name}: contains an unresolved template placeholder")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path.name}: may contain a credential or secret")
            break
    return text


def _json_object(text: str, name: str, errors: list[str]) -> dict:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"{name}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict) or not value:
        errors.append(f"{name}: must be a nonempty object")
        return {}
    return value


def _validate_images(bundle: Path, manifest: dict, prompts: dict[str, str], errors: list[str]) -> None:
    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append("reference_images.json: assets must contain approved image records")
        assets = []
    ids: set[str] = set()
    roles: set[str] = set()
    for asset in assets:
        if not isinstance(asset, dict):
            errors.append("reference_images.json: each asset must be an object")
            continue
        asset_id = asset.get("asset_id")
        if not isinstance(asset_id, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", asset_id):
            errors.append("reference_images.json: invalid asset_id")
            continue
        if asset_id in ids:
            errors.append(f"{asset_id}: duplicate image asset ID")
        ids.add(asset_id)
        role = asset.get("role")
        if role not in ("character", "environment", "prop", "keyframe", "style"):
            errors.append(f"{asset_id}: invalid image role")
        else:
            roles.add(role)
        approval = asset.get("approval")
        if not isinstance(approval, dict):
            approval = {}
        if approval.get("status") != "approved":
            errors.append(f"{asset_id}: reference image is not approved")
        if not isinstance(approval.get("source"), str) or not approval["source"].strip():
            errors.append(f"{asset_id}: missing explicit approval source")
        try:
            stamp = datetime.fromisoformat(str(approval.get("approved_at", "")).replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                raise ValueError("timezone required")
        except ValueError:
            errors.append(f"{asset_id}: invalid approval timestamp (timezone required)")
        path = asset.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"{asset_id}: missing image path")
            continue
        image = (bundle / path).resolve()
        image_root = (bundle / "references" / "images").resolve()
        if Path(path).is_absolute() or not image_root.is_relative_to(bundle) or not image.is_relative_to(image_root):
            errors.append(f"{asset_id}: image path must stay under references/images/")
            continue
        if image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"} or not image.is_file():
            errors.append(f"{asset_id}: missing or unsupported image file")
            continue
        try:
            data = image.read_bytes()
        except OSError as exc:
            errors.append(f"{asset_id}: cannot read image: {exc}")
            continue
        if not (data.startswith(b"\x89PNG\r\n\x1a\n") or data.startswith(b"\xff\xd8\xff") or (data.startswith(b"RIFF") and data[8:12] == b"WEBP")):
            errors.append(f"{asset_id}: file is not a recognized image")
        digest = hashlib.sha256(data).hexdigest()
        if asset.get("sha256") != digest:
            errors.append(f"{asset_id}: image hash changed or missing; reapprove this version")
    if not {"character", "environment"}.issubset(roles):
        errors.append("reference_images.json: approved character and environment images are required")
    mappings = manifest.get("scene_refs")
    if not isinstance(mappings, dict):
        errors.append("reference_images.json: scene_refs must be an object")
        mappings = {}
    if set(mappings) != set(prompts):
        errors.append("reference_images.json: scene_refs must match all scene IDs exactly")
    for scene_id, prompt in prompts.items():
        refs = mappings.get(scene_id)
        if not isinstance(refs, list) or not refs:
            errors.append(f"{scene_id}: missing approved image references")
            continue
        ingredients = re.search(r"^-\s*Ingredients:\s*(.+)$", prompt, re.M)
        attached = set(re.findall(r"[A-Za-z][A-Za-z0-9_-]*", ingredients.group(1))) if ingredients else set()
        for ref in refs:
            if not isinstance(ref, str) or ref not in ids:
                errors.append(f"{scene_id}: unknown image asset ID {ref!r}")
            elif ref not in attached:
                errors.append(f"{scene_id}: Ingredients does not include approved asset {ref}")


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
    scene_texts: dict[str, str] = {}
    for path in prompt_files:
        match = SCENE_FILE.fullmatch(path.name)
        if match:
            scene_numbers.append(int(match.group(1)))
        else:
            errors.append(f"Invalid scene prompt filename: {path.name}")

        text = _read_text(path, errors)
        scene_texts[path.stem] = text
        normalized = text.lower()
        if "Post only:" not in text:
            errors.append(f"{path.name}: missing post-production overlay line")
        if not re.search(r"no generated [^.\n]{0,80}(?:text|words)", normalized):
            errors.append(f"{path.name}: missing generated-text guardrail")
        if not re.search(r"-\s*Length:\s*\*\*\d+", text):
            errors.append(f"{path.name}: missing numeric clip length")
        if not re.search(r"-\s*Aspect:\s*\*\*[^*]+\*\*", text):
            errors.append(f"{path.name}: missing aspect ratio")

    actual_count = len(prompt_files)
    if not actual_count:
        errors.append("At least one scene prompt is required")
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
    if "audio mode" not in readme.lower():
        errors.append("README.md: missing audio mode")

    characters = texts.get("characters.md", "")
    if "Preserve the exact same" not in characters:
        errors.append("characters.md: missing explicit identity-preservation rule")

    master = texts.get("master_prompt_sheet.md", "")
    for field in ("scene_id", "duration", "aspect", "model", "audio_mode", "prompt", "ingredients", "extend-to"):
        if field not in master:
            errors.append(f"master_prompt_sheet.md: missing table field '{field}'")

    intake = texts.get("clip_intake.md", "")
    if "scene_01.mp4" not in intake:
        errors.append("clip_intake.md: missing deterministic scene filename")

    checkpoint_path = bundle / "checkpoint.json"
    checkpoint: dict[str, object] = {}
    if checkpoint_path.is_file():
        checkpoint = _json_object(texts.get("checkpoint.json", ""), "checkpoint.json", errors)

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
        audio_mode = checkpoint.get("audio_mode")
        if not isinstance(audio_mode, str) or audio_mode not in AUDIO_MODES:
            errors.append("checkpoint.json: choose a supported audio_mode")
        if "return_silent_videos" in checkpoint:
            errors.append("checkpoint.json: replace legacy return_silent_videos with audio_mode")
        scene_modes = checkpoint.get("scene_audio_modes", {})
        if not isinstance(scene_modes, dict):
            errors.append("checkpoint.json: scene_audio_modes must be an object")
            scene_modes = {}
        for scene_id, mode in scene_modes.items():
            if scene_id not in scene_texts or not isinstance(mode, str) or mode not in AUDIO_MODES:
                errors.append(f"checkpoint.json: invalid scene audio override for {scene_id}")
        review = checkpoint.get("dialogue_review")
        if audio_mode != "silent" or any(mode != "silent" for mode in scene_modes.values()):
            if not isinstance(review, dict) or review.get("status") != "reviewed":
                errors.append("checkpoint.json: natural-dialogue review is required")
            elif review.get("method") not in ("text_readthrough", "audio_readthrough") or not isinstance(review.get("notes"), str) or not review["notes"].strip():
                errors.append("checkpoint.json: dialogue review needs a method and concrete notes")
        for scene_id, text in scene_texts.items():
            scene_mode = scene_modes.get(scene_id, audio_mode)
            mode_match = re.search(r"^-\s*Audio mode:\s*\*\*([^*]+)\*\*", text, re.M)
            if not mode_match or mode_match.group(1) != scene_mode:
                errors.append(f"{scene_id}: audio mode must match checkpoint")
            if scene_mode == "native_dialogue" and re.search(r"return silent video|\bno audio\b|silently act", text, re.I):
                errors.append(f"{scene_id}: native dialogue conflicts with forced silence")
            if scene_mode == "silent" and "return silent video" not in text.lower():
                errors.append(f"{scene_id}: explicitly silent mode needs a silent-output instruction")
            if scene_mode != "silent" and not re.search(r"Dialogue:\s*\S", text):
                errors.append(f"{scene_id}: missing dialogue content")
        files = checkpoint.get("files")
        if not isinstance(files, list):
            errors.append("checkpoint.json: files must be an array")
        else:
            expected_paths = {f"prompts/{path.name}" for path in prompt_files} | set(REQUIRED_FILES)
            listed = {str(item) for item in files}
            missing = sorted(expected_paths - listed)
            if missing:
                errors.append(
                    "checkpoint.json: files is missing required entries: "
                    + ", ".join(missing)
                )

    if "reference_images.json" in texts:
        manifest = _json_object(texts["reference_images.json"], "reference_images.json", errors)
        _validate_images(bundle, manifest, scene_texts, errors)
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
