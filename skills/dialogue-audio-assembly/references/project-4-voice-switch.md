# Project 4: expert voice switches in the analysis section

This is a diagnostic example, not a universal set of timestamps or a preapproved voice for future projects.

In the 2026-09-29 Project 4 dubbing pass, the middle expert section contained 22 mapped turns. The v2 selection manifest marked 14 as original source speech and 8 as an alternate OmniVoice take. A later v3 patch inserted more continuous source audio to restore swallowed words. Both decisions addressed local wording/timing defects, but the repeated source changes made one on-screen expert sound like several speakers. File and profile names alone did not reveal the audible problem; the per-turn provenance map did.

For an audio-only review, four adjacent topic-sized expert takes were generated using one Project 4 expert profile, then split at ASR word boundaries and placed into the current source-time slots. Three takes generated an extra leading “Nói”; it was trimmed before assembly. The section WAV was delivered separately because the user requested audio. ASR confirmed the main text and absence of that leading word, but did **not** certify that the voice sounded right; the user must listen and accept the candidate. Previous v3 source and dialogue WAVs remain recoverable.

The transferable rule: **a fallback that fixes one phrase can break speaker identity across a section**. Before accepting any source/generated fallback, audit the neighboring turns and listen across the join. If the user asks only for WAV, check the WAV and stop there. Video rendering and audio-to-video alignment happen only when requested.
