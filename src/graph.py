
from collections import defaultdict


class MelodyGraph:
    def __init__(self):
        # Each interval points to the intervals that follow it.
        self.adjacency = defaultdict(set)

    def add_melody(self, intervals):
        """Add transitions between consecutive intervals."""
        for current_interval, next_interval in zip(
            intervals, intervals[1:]
        ):
            self.adjacency[current_interval].add(next_interval)

    def next_intervals(self, interval):
        """Return possible intervals that follow the given interval."""
        return self.adjacency.get(interval, set())

    def has_transition(self, current_interval, next_interval):
        """Check whether a transition exists."""
        return next_interval in self.adjacency.get(
            current_interval, set()
        )
