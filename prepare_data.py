"""Convert the local cleaned Nottingham ABC files to ``data/songs.json``."""

import argparse
from pathlib import Path

from src.loader import load_abc_folder, save_songs


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "nottingham")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "songs.json")
    args = parser.parse_args()

    songs = load_abc_folder(args.input)
    if not songs:
        raise SystemExit(f"No valid tunes found in {args.input}; songs.json was not written.")
    save_songs(songs, args.output)
    print(f"Loaded {len(songs)} tunes; wrote {args.output}")
    print(f"Example: {songs[0]['id']} — {songs[0]['title']} ({len(songs[0]['pitches'])} pitches)")


if __name__ == "__main__":
    main()
