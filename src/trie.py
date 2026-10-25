
class TrieNode:
    def __init__(self):
        self.children = {}
        self.song_ids = set()
        # Positions are (song_index, interval_offset) pairs. Keeping these on
        # the short seed nodes lets the engine retrieve substring candidates
        # without materializing every suffix of every tune.
        self.positions = set()


class MelodyTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, intervals, song_id):
        """Insert a sequence of musical intervals for a song."""
        node = self.root

        for interval in intervals:
            if interval not in node.children:
                node.children[interval] = TrieNode()

            node = node.children[interval]
            node.song_ids.add(song_id)

    def search(self, intervals):
        """Return song IDs containing the indexed interval sequence."""
        node = self.root

        for interval in intervals:
            if interval not in node.children:
                return set()

            node = node.children[interval]

        return set(node.song_ids)

    def insert_window(self, intervals, song_id, position):
        """Index a short interval window and the position where it occurs."""
        node = self.root
        for interval in intervals:
            node = node.children.setdefault(interval, TrieNode())
        node.song_ids.add(song_id)
        node.positions.add(position)

    def search_positions(self, intervals):
        """Return indexed positions for an exact window, or an empty set."""
        node = self.root
        for interval in intervals:
            node = node.children.get(interval)
            if node is None:
                return set()
        return set(node.positions)
