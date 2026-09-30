---
name: dialogue-audio-assembly
description: Assemble or repair Vietnamese dialogue WAVs for training videos when turns must stay in sync and each character must keep one voice. Use for OmniVoice pickups, mixed source/generated speech, missing words, clipped tails, audio-only deliverables, or dubbing timelines; video rendering is a separate requested step.
---

# Dialogue Audio Assembly

Make a dialogue track that says the approved words, keeps each character's voice stable, and fits the **current** source timeline. Preserve the last good media and deliver only the format requested. If the user asks for audio, finish with WAV; do not render or mux video as a routine check.

## 1. Establish the exact edit

1. Identify the file the user is actually reviewing, its duration, sample rate, channels, and any title-card offset. A time reported on the finished film may differ from source time. Confirm by dialogue and waveform before editing; never reuse timecodes from an older cut without remapping.
2. Write the edit scope: affected speaker and interval, words that must remain exact, approved voice/reference, and whether the output is a standalone pickup, section WAV, full dialogue WAV, or video. Preserve the source and previous export; use a new versioned output path.
3. Create a turn map with `section, speaker, approved text, source-time start/end, chosen take, profile identity, audible speech bounds, intended placement, and status`. Mark each take as original or generated. One clock and one source version must govern the map.

## 2. Lock voice before selecting lines

- Assign one accepted voice identity to each character across a continuous section. Record the exact profile/reference file and hash or other stable ID. Treat source speech and a clone as **different voice sources** until listening confirms they match. Never silently alternate original and generated takes sentence by sentence just because one take has better ASR or timing.
- For a voice-switch complaint, audit the turn map first: list consecutive turns with their source/profile. Replace the **smallest continuous region** that contains the unwanted switches with one voice source. Keep other speakers and sections as they were.
- Generate several short adjacent utterances as a coherent topic-sized take when independent generation makes timbre jump. Split the resulting take at real word/phrase boundaries for placement, preserving its shared voice quality. A short acknowledgment can stay with the neighboring exchange; do not synthesize filler to make it longer.
- An approved voice from another project is not automatically approved here. Present a candidate WAV for human judgment when the current project has no confirmed profile. Do not label a voice consistent merely because filenames or model settings match.

## 3. Prepare speech at natural pace

Generate with natural duration first; save raw take and the intended text. Do not force every line into a fixed video slot during generation. Check the first word, last syllable, brand/number pronunciation, filler and invented leading words. Trim only verified silence or unwanted speech, leaving a small audible tail. ASR helps locate omissions and word bounds but cannot certify pronunciation or speaker identity; listen when playback is available and describe an ASR-only check honestly.

If a take exceeds its slot, first use a genuine neighboring pause or group the thought differently. Mild tempo adjustment is a last local fit decision, checked for audible distortion and full final syllables. If it still will not fit, regenerate or revise the shot timing when authorized; do not swallow words, layer turns, or cut a consonant to satisfy a timestamp.

## 4. Assemble on a single timeline

1. Decode inputs to a common PCM sample rate/channel layout. Keep source time, output time and any card offsets distinct. Place by **audible speech bounds**, not WAV file length, TTS requested duration or ASR segment end alone.
2. Clear only the source dialogue being replaced so old and new voices cannot overlap. Preserve other speakers and approved ambience/music layers; if those are baked into the same track, inspect the replacement edges and restore the bed deliberately.
3. Place each take at the mapped start. Check available space through the next turn and the complete tail. Put cuts/crossfades in quiet boundaries; a short fade can remove clicks but must not fade away initial or final phonemes. Reject accidental overlap, duplicated words and unnatural empty gaps.
4. Set a coherent level for the speaker or section, then adjust exceptional takes only when measured and heard. Per-line RMS matching can produce audible pumping and make one character seem like several voices. Keep dialogue and music separate until the requested final mix.
5. Export a new WAV and a placement manifest recording source files, profile, speech bounds, placements, tempo/gain changes, replaced interval and preservation of the previous version. Do not treat a successful render as proof of correct speech.

## 5. Release checks

Run the bundled [timeline checker](scripts/check_timeline.py) on the placement manifest and current WAV. It checks bounds, overlaps, duplicated turns, section voice-source changes, and whether placed intervals contain audio. For an **authorized video mix**, give it several `source:output` anchors outside title cards and compare the dialogue WAV with the rendered audio by cross-correlation:

```bash
python3 scripts/check_timeline.py placements placement_manifest.json --track dialogue.wav --speaker expert --section analysis --expected-turns 22
python3 scripts/check_timeline.py align dialogue.wav current_video.mp4 --anchor 20:22 --anchor 110:116
```

Use anchors and expected counts from the **current** project; those numbers only illustrate the syntax. `align` can measure lag only where both files contain the same speech waveform. If speech was regenerated between the reference and render, compare the *new dialogue WAV* with its render, not the old source speech. Low correlation means alignment is unverified, not that the voices match. The checker does not certify words, pronunciation, timbre or lip sync; those still need the content and listening checks below.

- **Content:** compare every edited line with approved text. Check no inserted word, omitted word, doubled voice or clipped ending. ASR is a locating aid; human listening is the acceptance check for tone, identity and pronunciation.
- **Continuity:** hear the whole edited region, plus both entry and exit joins, at normal speed. Verify one stable speaker voice throughout the intended section. A profile ID alone is insufficient because separately generated short takes can drift.
- **Timing:** inspect waveform and placement manifest for overlap/gaps, compare several audible onsets to the current video only if video alignment was requested, and measure any render lag before compensating it. Do not carry a fixed lag value between renders.
- **Preservation:** compare unaffected regions against the prior WAV; report any codec or PCM round-trip differences rather than claiming bit identity. If video is requested later, check it separately after mux/render.
- **Delivery:** provide the exact requested WAV or video path and the previous recoverable version. State whether the audio was directly listened to or checked only with ASR/waveform. A user request for WAV does not authorize a new video export.

For the actual Project 4 voice-switch failure and its limits, read [the case note](references/project-4-voice-switch.md) when diagnosing mixed expert voices. For visual edits or Remotion composition, use the parent project's `video-spec` post-production guidance after audio acceptance.
