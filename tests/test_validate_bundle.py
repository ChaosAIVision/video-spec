from __future__ import annotations

import importlib.util
import base64
import hashlib
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "skills" / "video-spec" / "scripts" / "validate_bundle.py"
SPEC = importlib.util.spec_from_file_location("validate_bundle", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateBundleTests(unittest.TestCase):
    def make_bundle(self, root: Path, scene_count: int = 2) -> Path:
        bundle = root / "flow_handoff"
        prompts = bundle / "prompts"
        prompts.mkdir(parents=True)

        (bundle / "README.md").write_text(
            "# Handoff\n\nAudio mode: native_dialogue\n", encoding="utf-8"
        )
        (bundle / "characters.md").write_text(
            "# Characters\n\nPreserve the exact same face and wardrobe.\n",
            encoding="utf-8",
        )
        (bundle / "master_prompt_sheet.md").write_text(
            "| scene_id | duration | aspect | model | audio_mode | prompt | ingredients | extend-to |\n",
            encoding="utf-8",
        )
        (bundle / "clip_intake.md").write_text(
            "# Intake\n\nscene_01.mp4\n", encoding="utf-8"
        )

        prompt_entries = []
        for number in range(1, scene_count + 1):
            name = f"scene_{number:02d}.md"
            (prompts / name).write_text(
                "\n".join(
                    [
                        f"# Scene {number}",
                        "- Length: **8 seconds**",
                        "- Aspect: **9:16**",
                        "- Model: **Selected Flow model**",
                        "- Audio mode: **native_dialogue**",
                        "- Ingredients: character_agent, environment_office",
                        "",
                        "```text",
                        "Generate audible Vietnamese dialogue. No generated text.",
                        "Dialogue: Agent: Dạ, chị đang dùng loại nào ạ?",
                        "```",
                        "",
                        "Post only: Nhãn tiếng Việt có dấu",
                    ]
                ),
                encoding="utf-8",
            )
            prompt_entries.append(f"prompts/{name}")

        checkpoint = {
            "version": "1.1",
            "exit": "flow_handoff",
            "status": "completed",
            "mode": "spec-only",
            "generation_api_calls": 0,
            "cost_usd": 0,
            "scene_count": scene_count,
            "aspect_ratio": "9:16",
            "audio_mode": "native_dialogue",
            "dialogue_review": {
                "status": "reviewed",
                "method": "text_readthrough",
                "notes": "Shortened the consultant question and checked consistent em/chị address.",
            },
            "files": [
                "README.md",
                "characters.md",
                "master_prompt_sheet.md",
                "clip_intake.md",
                "checkpoint.json",
                "reference_images.json",
                *prompt_entries,
            ],
        }
        (bundle / "checkpoint.json").write_text(
            json.dumps(checkpoint, ensure_ascii=False), encoding="utf-8"
        )
        images = bundle / "references" / "images"
        images.mkdir(parents=True)
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=")
        assets = []
        for asset_id, role in (("character_agent", "character"), ("environment_office", "environment")):
            path = images / f"{asset_id}.png"
            path.write_bytes(png)
            assets.append({
                "asset_id": asset_id,
                "role": role,
                "path": path.relative_to(bundle).as_posix(),
                "sha256": hashlib.sha256(png).hexdigest(),
                "approval": {"status": "approved", "source": "test fixture user approval", "approved_at": "2026-09-22T10:00:00+07:00"},
            })
        manifest = {"version": "1.0", "assets": assets, "scene_refs": {
            f"scene_{number:02d}": ["character_agent", "environment_office"]
            for number in range(1, scene_count + 1)
        }}
        (bundle / "reference_images.json").write_text(json.dumps(manifest), encoding="utf-8")
        return bundle

    def test_valid_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            self.assertEqual(VALIDATOR.validate_bundle(bundle, 2), [])

    def test_rejects_escaped_unicode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            prompt = bundle / "prompts" / "scene_01.md"
            prompt.write_text(prompt.read_text(encoding="utf-8") + r" \u0111", encoding="utf-8")
            errors = VALIDATOR.validate_bundle(bundle, 2)
            self.assertTrue(any("escaped Unicode" in error for error in errors))

    def test_rejects_forced_silence_in_native_dialogue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            prompt = bundle / "prompts" / "scene_02.md"
            prompt.write_text(
                prompt.read_text(encoding="utf-8") + "\nReturn silent video. No audio.\n",
                encoding="utf-8",
            )
            errors = VALIDATOR.validate_bundle(bundle, 2)
            self.assertTrue(any("conflicts with forced silence" in error for error in errors))

    def test_accepts_case_variation_in_guardrails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            prompt = bundle / "prompts" / "scene_01.md"
            prompt.write_text(
                prompt.read_text(encoding="utf-8")
                .replace("No generated text", "no generated text"),
                encoding="utf-8",
            )
            self.assertEqual(VALIDATOR.validate_bundle(bundle, 2), [])

    def test_accepts_equivalent_generated_text_guardrail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            prompt = bundle / "prompts" / "scene_01.md"
            prompt.write_text(
                prompt.read_text(encoding="utf-8").replace(
                    "No generated text", "No generated quotation marks or text"
                ),
                encoding="utf-8",
            )
            self.assertEqual(VALIDATOR.validate_bundle(bundle, 2), [])

    def test_rejects_nonconsecutive_scenes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            (bundle / "prompts" / "scene_02.md").rename(
                bundle / "prompts" / "scene_03.md"
            )
            errors = VALIDATOR.validate_bundle(bundle, 2)
            self.assertTrue(any("consecutively numbered" in error for error in errors))

    def mutate_json(self, bundle: Path, name: str, mutate) -> None:
        path = bundle / name
        value = json.loads(path.read_text(encoding="utf-8"))
        mutate(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def test_rejects_pending_or_missing_image_approval(self) -> None:
        for field in ("status", "source", "approved_at"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                bundle = self.make_bundle(Path(tmp))
                self.mutate_json(bundle, "reference_images.json", lambda data: data["assets"][0]["approval"].pop(field))
                self.assertTrue(VALIDATOR.validate_bundle(bundle, 2))

    def test_rejects_changed_reference_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            image = bundle / "references/images/character_agent.png"
            image.write_bytes(image.read_bytes() + b"changed")
            self.assertTrue(any("reapprove" in e for e in VALIDATOR.validate_bundle(bundle, 2)))

    def test_rejects_missing_reference_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            (bundle / "references/images/character_agent.png").unlink()
            self.assertTrue(any("missing or unsupported image" in e for e in VALIDATOR.validate_bundle(bundle, 2)))

    def test_rejects_missing_or_unknown_scene_reference(self) -> None:
        for refs in ([], ["unknown_asset"]):
            with self.subTest(refs=refs), tempfile.TemporaryDirectory() as tmp:
                bundle = self.make_bundle(Path(tmp))
                self.mutate_json(bundle, "reference_images.json", lambda data: data["scene_refs"].update(scene_01=refs))
                self.assertTrue(VALIDATOR.validate_bundle(bundle, 2))

    def test_rejects_unattached_approved_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            prompt = bundle / "prompts/scene_01.md"
            prompt.write_text(prompt.read_text().replace("- Ingredients: character_agent, environment_office", "- Ingredients: environment_office"))
            self.assertTrue(any("Ingredients" in e for e in VALIDATOR.validate_bundle(bundle, 2)))

    def test_rejects_unreviewed_dialogue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            self.mutate_json(bundle, "checkpoint.json", lambda data: data.pop("dialogue_review"))
            self.assertTrue(any("natural-dialogue review" in e for e in VALIDATOR.validate_bundle(bundle, 2)))

    def test_rejects_unresolved_dialogue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            prompt = bundle / "prompts/scene_01.md"
            prompt.write_text(prompt.read_text() + "\n{{VIETNAMESE_DIALOGUE}}\n")
            self.assertTrue(any("unresolved template" in e for e in VALIDATOR.validate_bundle(bundle, 2)))

    def test_other_audio_modes_are_supported_when_selected(self) -> None:
        for mode in ("voiceover", "dubbed_dialogue", "silent"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                bundle = self.make_bundle(Path(tmp))
                self.mutate_json(bundle, "checkpoint.json", lambda data: data.update(audio_mode=mode))
                for prompt in (bundle / "prompts").glob("*.md"):
                    text = prompt.read_text().replace("**native_dialogue**", f"**{mode}**")
                    if mode == "silent":
                        text = text.replace("Generate audible Vietnamese dialogue.", "Return silent video.")
                        text = text.replace("Dialogue: Agent: Dạ, chị đang dùng loại nào ạ?", "")
                    prompt.write_text(text)
                self.assertEqual(VALIDATOR.validate_bundle(bundle, 2), [])

    def test_rejects_mismatched_audio_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            self.mutate_json(bundle, "checkpoint.json", lambda data: data.update(audio_mode="voiceover"))
            self.assertTrue(any("audio mode must match" in e for e in VALIDATOR.validate_bundle(bundle, 2)))

    def test_accepts_approved_expert_voiceover_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            self.mutate_json(bundle, "checkpoint.json", lambda data: data.update(scene_audio_modes={"scene_02": "voiceover"}))
            prompt = bundle / "prompts/scene_02.md"
            prompt.write_text(prompt.read_text().replace("**native_dialogue**", "**voiceover**").replace("Generate audible Vietnamese dialogue.", "Generate Vietnamese expert voiceover; on-screen characters do not speak.").replace("Dialogue: Agent: Dạ, chị đang dùng loại nào ạ?", "Dialogue: Expert: Hãy hỏi rõ điều khách đang băn khoăn."))
            self.assertEqual(VALIDATOR.validate_bundle(bundle, 2), [])

    def test_rejects_invalid_checkpoint_shape(self) -> None:
        for value in ({}, [], None):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as tmp:
                bundle = self.make_bundle(Path(tmp))
                (bundle / "checkpoint.json").write_text(json.dumps(value))
                self.assertTrue(any("nonempty object" in e for e in VALIDATOR.validate_bundle(bundle, 2)))


if __name__ == "__main__":
    unittest.main()
