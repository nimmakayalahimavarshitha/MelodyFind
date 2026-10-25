# Nottingham dataset

Source: [JukeDeck's cleaned Nottingham dataset](https://github.com/jukedeck/nottingham-dataset), based on the [Nottingham Music Database](http://abc.sourceforge.net/NMD/). Version: the upstream `master` snapshot extracted on 24 October 2026; the archive has no Git metadata or release tag, so its commit cannot be identified. The cleaned source contains 14 ABC collection files in `ABC_cleaned/`.

Copy those `.abc` files into the local, Git-ignored `data/nottingham/` folder, then run `python prepare_data.py`. The converter parses tunes with `music21`, removes quoted chord annotations, uses the top pitch for any parsed chord, skips tunes that do not parse or have fewer than eight notes, and writes integer MIDI pitches to `data/songs.json`.

The generated records use this repository engine's schema: unique integer `id`, `title`, `pitches` (integer MIDI list), plus `source`, `key`, `meter`, and `length`. The engine expects `id`; the separate starter project uses `song_id`.

The JukeDeck dataset repository is released under **GNU GPL-3.0**. Its README credits the Nottingham Music Database as the original source and retains individual transcriber/source names in ABC `S:` fields. Keep the upstream `LICENSE.md` and README with the original archive when redistributing source data. No raw ABC files are tracked here.
