
def rolling_hash(sequence, base=257, mod=1_000_000_007):
    """Calculate a hash for a sequence of MIDI pitch values."""
    if not sequence:
        raise ValueError("Sequence cannot be empty")

    result = 0
    for value in sequence:
        result = (result * base + value) % mod

    return result


def rolling_hashes(sequence, window_size, base=257, mod=1_000_000_007):
    """Generate rolling hashes for consecutive melody windows."""
    if window_size <= 0:
        raise ValueError("Window size must be positive")

    if window_size > len(sequence):
        return []

    result = []
    current_hash = rolling_hash(sequence[:window_size], base, mod)
    highest_power = pow(base, window_size - 1, mod)

    result.append((0, current_hash))

    for start in range(1, len(sequence) - window_size + 1):
        outgoing = sequence[start - 1]
        incoming = sequence[start + window_size - 1]

        current_hash = (
            (current_hash - outgoing * highest_power) * base + incoming
        ) % mod

        result.append((start, current_hash))

    return result


if __name__ == "__main__":
    melody = [60, 62, 64, 65, 67]

    print("Melody:", melody)
    print("Whole melody hash:", rolling_hash(melody))
    print("Window hashes:", rolling_hashes(melody, 3))
