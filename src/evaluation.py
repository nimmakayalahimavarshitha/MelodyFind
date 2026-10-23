
def calculate_accuracy(total_queries, correct_matches):
    if total_queries <= 0:
        raise ValueError("Total queries must be greater than zero")

    if correct_matches < 0 or correct_matches > total_queries:
        raise ValueError("Correct matches must be between zero and total queries")

    return (correct_matches / total_queries) * 100


def evaluate_results(expected_songs, predicted_songs):
    if len(expected_songs) != len(predicted_songs):
        raise ValueError("Expected and predicted lists must have the same length")

    if not expected_songs:
        raise ValueError("Song lists cannot be empty")

    correct = sum(
        expected == predicted
        for expected, predicted in zip(expected_songs, predicted_songs)
    )

    accuracy = calculate_accuracy(len(expected_songs), correct)

    return {
        "total_queries": len(expected_songs),
        "correct_matches": correct,
        "incorrect_matches": len(expected_songs) - correct,
        "accuracy_percent": round(accuracy, 2),
    }
