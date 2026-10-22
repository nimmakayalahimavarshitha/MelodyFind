
import unittest

from src.rolling_hash import rolling_hash, rolling_hashes


class TestRollingHash(unittest.TestCase):

    def test_hash_normal_melody(self):
        melody = [60, 62, 64]
        self.assertIsInstance(rolling_hash(melody), int)

    def test_empty_sequence(self):
        with self.assertRaises(ValueError):
            rolling_hash([])

    def test_window_hashes(self):
        melody = [60, 62, 64, 65, 67]
        result = rolling_hashes(melody, 3)

        self.assertEqual(len(result), 3)
        self.assertEqual(
            result,
            [
                (0, rolling_hash([60, 62, 64])),
                (1, rolling_hash([62, 64, 65])),
                (2, rolling_hash([64, 65, 67])),
            ],
        )

    def test_window_larger_than_melody(self):
        self.assertEqual(rolling_hashes([60, 62], 3), [])

    def test_zero_window_size(self):
        with self.assertRaises(ValueError):
            rolling_hashes([60, 62, 64], 0)

    def test_negative_window_size(self):
        with self.assertRaises(ValueError):
            rolling_hashes([60, 62, 64], -1)


if __name__ == "__main__":
    unittest.main()
