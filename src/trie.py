
class TrieNode:
    def __init__(self):
        self.children = {}
        self.song_ids = set()


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
