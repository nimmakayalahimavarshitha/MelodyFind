
import unittest

from src.engine import MelodySearchEngine


class TestMelodySearchEngine(unittest.TestCase):
    def setUp(self):
        self.songs = [
            {
                "id": "song1",
                "title": "Tune A",
                "pitches": [60, 62, 65, 64],
            },
            {
                "id": "song2",
                "title": "Tune B",
                "pitches": [55, 57, 60, 59],
            },
            {
                "id": "song3",
                "title": "Tune C",
                "pitches": [60, 61, 64],
            },
        ]
        self.engine = MelodySearchEngine(self.songs)

    def test_transposed_melody_matches(self):
        results = self.engine.search([72, 74, 77])
        self.assertEqual(
            {song["id"] for song in results},
            {"song1", "song2"},
        )

    def test_fragment_in_middle_of_song(self):
        results = self.engine.search([65, 64])
        self.assertEqual(
            {song["id"] for song in results},
            {"song1", "song2"},
        )

    def test_no_match(self):
        results = self.engine.search([60, 63, 68])
        self.assertEqual(results, [])

    def test_empty_query(self):
        self.assertEqual(self.engine.search([]), [])

    def test_single_note_query(self):
        results = self.engine.search([60])
        self.assertEqual(
            {song["id"] for song in results},
            {"song1", "song2", "song3"},
        )


if __name__ == "__main__":
    unittest.main()
