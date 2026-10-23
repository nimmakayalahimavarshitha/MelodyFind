
import unittest
from src.evaluation import calculate_accuracy, evaluate_results


class TestEvaluation(unittest.TestCase):

    def test_accuracy(self):
        self.assertEqual(calculate_accuracy(10, 8), 80.0)

    def test_all_matches_correct(self):
        result = evaluate_results(["Song A", "Song B"], ["Song A", "Song B"])
        self.assertEqual(result["accuracy_percent"], 100.0)

    def test_some_matches_incorrect(self):
        result = evaluate_results(["Song A", "Song B"], ["Song A", "Song C"])
        self.assertEqual(result["correct_matches"], 1)
        self.assertEqual(result["accuracy_percent"], 50.0)

    def test_zero_queries(self):
        with self.assertRaises(ValueError):
            calculate_accuracy(0, 0)

    def test_different_list_lengths(self):
        with self.assertRaises(ValueError):
            evaluate_results(["Song A"], ["Song A", "Song B"])


if __name__ == "__main__":
    unittest.main()
