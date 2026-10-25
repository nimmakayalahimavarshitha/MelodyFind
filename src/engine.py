
from src.graph import MelodyGraph
from src.hash_table import CustomHashTable
from src.rolling_hash import rolling_hash
from src.trie import MelodyTrie


def to_intervals(pitches):
    """Convert MIDI pitches into consecutive pitch differences."""
    return [
        pitches[i + 1] - pitches[i]
        for i in range(len(pitches) - 1)
    ]


class MelodySearchEngine:
    def __init__(self, songs):
        self.songs = songs
        self.graph = MelodyGraph()
        self.trie = MelodyTrie()
        self.hash_table = CustomHashTable()
        self._song_intervals = []
        # Index only one- and two-interval seed windows. This keeps index size
        # linear in the corpus rather than storing every possible fragment.
        for song_index, song in enumerate(self.songs):
            intervals = to_intervals(song["pitches"])
            self._song_intervals.append((song, intervals))
            self.graph.add_melody(intervals)
            for offset, interval in enumerate(intervals):
                self._index_window((interval,), song_index, offset)
                if offset + 1 < len(intervals):
                    self._index_window(
                        (interval, intervals[offset + 1]), song_index, offset
                    )

    def _index_window(self, window, song_index, offset):
        position = (song_index, offset)
        self.trie.insert_window(window, song_index, position)
        key = (len(window), rolling_hash(window))
        self.hash_table.insert(key, position)

    def search(self, query_pitches):
        """Return songs containing the query's interval pattern."""
        if not query_pitches:
            return []

        query_intervals = to_intervals(query_pitches)

        # A single note has no interval pattern.
        if not query_intervals:
            return list(self.songs)

        # Every adjacent transition must exist in the corpus graph. This is a
        # cheap rejection step before consulting the positional indexes.
        if any(
            not self.graph.has_transition(current, following)
            for current, following in zip(query_intervals, query_intervals[1:])
        ):
            return []

        # Trie traversal locates the exact short seed; the custom hash table
        # independently narrows it to windows with the same rolling hash.
        # Intersecting both postings makes each structure part of candidate
        # retrieval. Full seed and melody comparisons below guard collisions.
        seed = tuple(query_intervals[:min(2, len(query_intervals))])
        trie_positions = self.trie.search_positions(seed)
        key = (len(seed), rolling_hash(seed))
        hash_positions = {
            position
            for position in self.hash_table.search(key)
            if self._song_intervals[position[0]][1][
                position[1]:position[1] + len(seed)
            ] == list(seed)
        }
        candidate_positions = trie_positions & hash_positions

        matching_song_indexes = set()
        query_length = len(query_intervals)
        for song_index, offset in candidate_positions:
            intervals = self._song_intervals[song_index][1]
            if intervals[offset:offset + query_length] == query_intervals:
                matching_song_indexes.add(song_index)

        return [
            song
            for song_index, (song, _) in enumerate(self._song_intervals)
            if song_index in matching_song_indexes
        ]
