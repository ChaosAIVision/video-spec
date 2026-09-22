from __future__ import annotations

import importlib.util
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
            "# Handoff\n\nReturn silent videos ON\n", encoding="utf-8"
        )
        (bundle / "characters.md").write_text(
            "# Characters\n\nPreserve the exact same face and wardrobe.\n",
            encoding="utf-8",
        )
        (bundle / "master_prompt_sheet.md").write_text(
            "| scene_id | duration | aspect | model | prompt | ingredients | extend-to |\n",
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
                        "",
                        "```text",
                        "Return silent video. No generated text.",
                        "```",
                        "",
                        "Post only: Nhãn tiếng Việt có dấu",
                    ]
                ),
                encoding="utf-8",
            )
            prompt_entries.append(f"prompts/{name}")

        checkpoint = {
            "version": "1.0",
            "exit": "flow_handoff",
            "status": "completed",
            "mode": "spec-only",
            "generation_api_calls": 0,
            "cost_usd": 0,
            "scene_count": scene_count,
            "aspect_ratio": "9:16",
            "return_silent_videos": True,
            "files": [
                "README.md",
                "characters.md",
                "master_prompt_sheet.md",
                "clip_intake.md",
                *prompt_entries,
            ],
        }
        (bundle / "checkpoint.json").write_text(
            json.dumps(checkpoint, ensure_ascii=False), encoding="utf-8"
        )
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

    def test_rejects_missing_silent_instruction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            prompt = bundle / "prompts" / "scene_02.md"
            prompt.write_text(
                prompt.read_text(encoding="utf-8").replace("Return silent video. ", ""),
                encoding="utf-8",
            )
            errors = VALIDATOR.validate_bundle(bundle, 2)
            self.assertTrue(any("missing 'Return silent video'" in error for error in errors))

    def test_accepts_case_variation_in_guardrails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self.make_bundle(Path(tmp))
            prompt = bundle / "prompts" / "scene_01.md"
            prompt.write_text(
                prompt.read_text(encoding="utf-8")
                .replace("Return silent video", "return silent video")
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


if __name__ == "__main__":
    unittest.main()
