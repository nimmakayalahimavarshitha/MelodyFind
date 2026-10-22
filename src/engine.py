
from src.trie import MelodyTrie
from src.graph import MelodyGraph
from src.hash_table import CustomHashTable
from src.rolling_hash import rolling_hash, rolling_hashes


def to_intervals(pitches):
    """Convert MIDI pitches into consecutive pitch differences."""
    return [
        pitches[i + 1] - pitches[i]
        for i in range(len(pitches) - 1)
    ]


class MelodySearchEngine:
    def __init__(self, songs):
        self.songs = songs
        self.trie = MelodyTrie()
        self.graph = MelodyGraph()
        self.hash_table = CustomHashTable()
        self._build_index()

    def _build_index(self):
        """Index interval suffixes and every fragment hash."""
        for song in self.songs:
            intervals = to_intervals(song["pitches"])
            song_id = song["id"]

            self.graph.add_melody(intervals)

            # Trie: index every suffix for fragment searching.
            for start in range(len(intervals)):
                self.trie.insert(intervals[start:], song_id)

            # Hash table: index all fragment lengths.
            for window_size in range(1, len(intervals) + 1):
                for start, value in rolling_hashes(
                    intervals, window_size
                ):
                    fragment = intervals[start:start + window_size]
                    self.hash_table.insert(
                        (window_size, value),
                        (song_id, fragment)
                    )

    def search(self, query_pitches):
        """Return songs containing the query's interval pattern."""
        if not query_pitches:
            return []

        query_intervals = to_intervals(query_pitches)

        # A single note has no interval pattern.
        if not query_intervals:
            return list(self.songs)

        trie_ids = self.trie.search(query_intervals)

        key = (
            len(query_intervals),
            rolling_hash(query_intervals)
        )
        hash_entries = self.hash_table.search(key)

        # Verify full sequences to protect against hash collisions.
        hash_ids = {
            song_id
            for song_id, fragment in hash_entries
            if fragment == query_intervals
        }

        matching_ids = trie_ids & hash_ids

        return [
            song for song in self.songs
            if song["id"] in matching_ids
        ]
