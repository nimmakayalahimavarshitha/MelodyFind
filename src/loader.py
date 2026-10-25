"""Parse cleaned Nottingham ABC files into records for this repository's engine."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def split_abc_tunes(text: str) -> list[str]:
    """Split a collection ABC file into tune blocks starting at ``X:``."""
    chunks = re.split(r"(?m)^(?=X:\s*\S)", text)
    return [chunk for chunk in chunks if re.match(r"(?m)^X:\s*\S", chunk)]


def header(chunk: str, letter: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(letter)}:\s*(.+)$", chunk)
    return match.group(1).strip() if match else None


def tune_to_pitches(chunk: str) -> list[int]:
    """Parse one ABC tune and retain melody notes as integer MIDI pitches."""
    from music21 import chord, converter, note

    # Chord names are annotations, not melody notes.
    score = converter.parse(re.sub(r'"[^"]*"', "", chunk), format="abc")
    pitches: list[int] = []
    for element in score.flatten().notes:
        if isinstance(element, note.Note):
            pitches.append(int(element.pitch.midi))
        elif isinstance(element, chord.Chord):
            pitches.append(int(max(p.midi for p in element.pitches)))
    return pitches


def load_abc_folder(
    folder: str | Path, source: str = "Nottingham (JukeDeck cleaned ABC)", min_notes: int = 8
) -> list[dict[str, Any]]:
    """Read sorted ABC files and assign unique integer ``id`` values.

    The clone's ``MelodySearchEngine`` indexes ``song['id']``; this field is
    intentionally distinct from the starter project's ``song_id`` schema.
    """
    root = Path(folder)
    songs: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.abc")):
        text = path.read_text(encoding="latin-1")
        for chunk in split_abc_tunes(text):
            try:
                pitches = tune_to_pitches(chunk)
            except Exception:
                continue
            if len(pitches) < min_notes:
                continue
            song_id = len(songs)
            songs.append(
                {
                    "id": song_id,
                    "title": header(chunk, "T") or f"Tune {song_id}",
                    "source": source,
                    "key": header(chunk, "K"),
                    "meter": header(chunk, "M"),
                    "pitches": pitches,
                    "length": len(pitches),
                }
            )
    return songs


def save_songs(songs: list[dict[str, Any]], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(songs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_songs(path: str | Path) -> list[dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
