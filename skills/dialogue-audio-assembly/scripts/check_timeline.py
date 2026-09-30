#!/usr/bin/env python3
"""Check dialogue placements and measured audio lag on a current timeline.

Requires NumPy; the `align` command also requires FFmpeg.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import wave
from collections import defaultdict
from pathlib import Path

import numpy as np


def wav_info(path: Path) -> tuple[int, int, int, float]:
    with wave.open(str(path), 'rb') as handle:
        if handle.getsampwidth() != 2 or handle.getcomptype() != 'NONE':
            raise ValueError('Track must be uncompressed 16-bit PCM WAV')
        return handle.getframerate(), handle.getnchannels(), handle.getnframes(), handle.getnframes() / handle.getframerate()


def interval_rms_dbfs(path: Path, start: float, end: float) -> float:
    with wave.open(str(path), 'rb') as handle:
        rate = handle.getframerate()
        channels = handle.getnchannels()
        first = max(0, round(start * rate))
        last = min(handle.getnframes(), round(end * rate))
        if last <= first:
            return float('-inf')
        handle.setpos(first)
        audio = np.frombuffer(handle.readframes(last - first), dtype='<i2').astype(np.float64)
    audio = audio.reshape(-1, channels) / 32768.0
    rms = float(np.sqrt(np.mean(audio * audio)))
    return 20 * math.log10(rms) if rms else float('-inf')


def check_placements(manifest: dict, track: Path | None, overlap_tolerance: float,
                     minimum_rms_dbfs: float, expected_turns: int | None,
                     default_speaker: str | None, default_section: str | None,
                     from_time: float | None, to_time: float | None) -> dict:
    if isinstance(manifest, list):
        manifest = {'placements': manifest}
    rows = manifest.get('placements')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Manifest needs a nonempty placements list')
    errors: list[str] = []
    warnings: list[str] = []
    normalized = []
    identity_by_role: dict[tuple[str, str], set[str]] = defaultdict(set)
    turn_ids = []
    track_duration = wav_info(track)[3] if track else None
    replacement = manifest.get('replacement_source_time')

    for number, row in enumerate(rows, 1):
        label = row.get('id') or row.get('turns') or number
        try:
            start, end = float(row['start']), float(row['end'])
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f'{label}: invalid start/end ({exc})')
            continue
        if (from_time is not None and start < from_time) or (to_time is not None and start >= to_time):
            continue
        if not all(math.isfinite(value) for value in (start, end)) or start < 0 or end <= start:
            errors.append(f'{label}: invalid interval {start}..{end}')
        if track_duration is not None and end > track_duration + .002:
            errors.append(f'{label}: ends after WAV duration {track_duration:.3f}s')
        if replacement and (start < replacement[0] - .002 or end > replacement[1] + .002):
            errors.append(f'{label}: outside replacement interval {replacement}')
        speaker = row.get('speaker') or manifest.get('speaker') or default_speaker or 'unknown'
        section = row.get('section') or manifest.get('section') or default_section or 'unspecified'
        identity = (row.get('profile') or row.get('voice_source') or row.get('v2_source')
                    or row.get('source') or manifest.get('profile'))
        if identity:
            identity_by_role[(section, speaker)].add(str(identity))
        else:
            warnings.append(f'{label}: no profile/voice_source to audit')
        ids = row.get('turns') or [row.get('id', number)]
        turn_ids.extend(str(item) for item in ids)
        if track and start >= 0 and end <= track_duration + .002 and end > start:
            rms = interval_rms_dbfs(track, start, end)
            if rms < minimum_rms_dbfs:
                errors.append(f'{label}: low energy {rms:.1f} dBFS inside placement')
        normalized.append((start, end, bool(row.get('allow_overlap')), str(label)))

    normalized.sort(key=lambda item: item[0])
    gaps = []
    for previous, current in zip(normalized, normalized[1:]):
        overlap = previous[1] - current[0]
        if overlap > overlap_tolerance and not (previous[2] and current[2]):
            errors.append(f'{previous[3]} overlaps {current[3]} by {overlap:.3f}s')
        elif overlap < -.15:
            gaps.append({'after': previous[3], 'before': current[3], 'seconds': round(-overlap, 3)})
    for role, identities in identity_by_role.items():
        if len(identities) > 1:
            errors.append(f'{role[0]}/{role[1]} has multiple voice sources: {sorted(identities)}')
    if len(turn_ids) != len(set(turn_ids)):
        errors.append('Turn IDs are duplicated across placements')
    if expected_turns is not None and len(turn_ids) != expected_turns:
        errors.append(f'Expected {expected_turns} turns; found {len(turn_ids)}')
    return {
        'ok': not errors, 'placements': len(normalized), 'turns': len(turn_ids),
        'track_duration_seconds': track_duration,
        'voice_sources': {f'{section}/{speaker}': sorted(values) for (section, speaker), values in identity_by_role.items()},
        'gaps_for_review': gaps,
        'errors': errors, 'warnings': warnings,
    }


def decode_window(path: Path, start: float, seconds: float, rate: int) -> np.ndarray:
    command = [
        'ffmpeg', '-v', 'error', '-i', str(path), '-ss', f'{start:.6f}',
        '-t', f'{seconds:.6f}', '-vn', '-ac', '1', '-ar', str(rate), '-f', 'f32le', '-',
    ]
    audio = np.frombuffer(subprocess.check_output(command), dtype='<f4').astype(np.float64)
    if len(audio) < round(seconds * rate * .95):
        raise ValueError(f'{path}: too little audio at {start:.3f}s')
    return audio


def estimate_lag(reference: np.ndarray, rendered: np.ndarray, max_lag_samples: int) -> tuple[int, float]:
    size = min(len(reference), len(rendered))
    if max_lag_samples >= size or max_lag_samples < 0:
        raise ValueError('Lag search must be shorter than the comparison window')
    x, y = reference[:size], rendered[:size]
    x, y = x - x.mean(), y - y.mean()
    best = (0, float('-inf'))
    for lag in range(-max_lag_samples, max_lag_samples + 1):
        if lag >= 0:
            left, right = x[:size - lag], y[lag:size]
        else:
            left, right = x[-lag:size], y[:size + lag]
        score = float(np.dot(left, right) / (np.linalg.norm(left) * np.linalg.norm(right) + 1e-12))
        if score > best[1]:
            best = lag, score
    return best


def check_alignment(reference: Path, rendered: Path, anchors: list[tuple[float, float]],
                    seconds: float, rate: int, search_ms: float,
                    tolerance_ms: float, drift_tolerance_ms: float,
                    min_correlation: float) -> dict:
    samples = []
    errors = []
    for source_time, output_time in anchors:
        x = decode_window(reference, source_time, seconds, rate)
        y = decode_window(rendered, output_time, seconds, rate)
        lag, correlation = estimate_lag(x, y, round(search_ms * rate / 1000))
        lag_ms = lag * 1000 / rate
        samples.append({'source_time': source_time, 'output_time': output_time,
                        'lag_ms': round(lag_ms, 3), 'correlation': round(correlation, 4)})
        if correlation < min_correlation:
            errors.append(f'{source_time:g}s: correlation {correlation:.3f} is too low to certify alignment')
        elif abs(lag_ms) > tolerance_ms:
            errors.append(f'{source_time:g}s: lag {lag_ms:+.2f}ms exceeds ±{tolerance_ms:g}ms')
    reliable = [row['lag_ms'] for row in samples if row['correlation'] >= min_correlation]
    drift = max(reliable) - min(reliable) if len(reliable) > 1 else 0.0
    if drift > drift_tolerance_ms:
        errors.append(f'Lag varies by {drift:.2f}ms across anchors; limit is {drift_tolerance_ms:g}ms')
    return {'ok': not errors, 'samples': samples, 'errors': errors,
            'lag_drift_ms': round(drift, 3),
            'note': 'Correlation measures lag only where reference and render contain the same speech waveform.'}


def parse_anchor(value: str) -> tuple[float, float]:
    try:
        source, output = (float(item) for item in value.split(':', 1))
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Use SOURCE_SECONDS:OUTPUT_SECONDS') from exc
    if source < 0 or output < 0:
        raise argparse.ArgumentTypeError('Anchor times must be nonnegative')
    return source, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    placements = sub.add_parser('placements', help='Check placement bounds, overlaps, voice identity and WAV energy')
    placements.add_argument('manifest', type=Path)
    placements.add_argument('--track', type=Path, help='16-bit PCM dialogue WAV')
    placements.add_argument('--overlap-tolerance-ms', type=float, default=20)
    placements.add_argument('--min-rms-dbfs', type=float, default=-55)
    placements.add_argument('--expected-turns', type=int)
    placements.add_argument('--speaker', help='Speaker when the manifest has one global voice')
    placements.add_argument('--section', help='Section when the manifest has one global section')
    placements.add_argument('--from-time', type=float, help='Audit placements starting at or after this source time')
    placements.add_argument('--to-time', type=float, help='Audit placements starting before this source time')
    alignment = sub.add_parser('align', help='Measure render lag where source and output contain the same waveform')
    alignment.add_argument('reference', type=Path)
    alignment.add_argument('rendered', type=Path)
    alignment.add_argument('--anchor', type=parse_anchor, action='append', required=True,
                           help='SOURCE_SECONDS:OUTPUT_SECONDS, once per test window')
    alignment.add_argument('--window-seconds', type=float, default=5)
    alignment.add_argument('--sample-rate', type=int, default=4000)
    alignment.add_argument('--search-ms', type=float, default=200)
    alignment.add_argument('--tolerance-ms', type=float, default=20)
    alignment.add_argument('--drift-tolerance-ms', type=float, default=20)
    alignment.add_argument('--min-correlation', type=float, default=.75)
    args = parser.parse_args()
    try:
        if args.command == 'placements':
            result = check_placements(json.loads(args.manifest.read_text()), args.track,
                                      args.overlap_tolerance_ms / 1000, args.min_rms_dbfs,
                                      args.expected_turns, args.speaker, args.section,
                                      args.from_time, args.to_time)
        else:
            result = check_alignment(args.reference, args.rendered, args.anchor,
                                     args.window_seconds, args.sample_rate, args.search_ms,
                                     args.tolerance_ms, args.drift_tolerance_ms,
                                     args.min_correlation)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        result = {'ok': False, 'errors': [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
