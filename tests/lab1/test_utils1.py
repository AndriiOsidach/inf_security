from lab1.utils1 import calculate_period, estimate_pi, generate_system_sequence, gcd


def test_calculate_period():
    # Test with repeating sequence
    assert calculate_period([1, 2, 3, 1, 2, 3]) == 3
    # Test with no repetition
    assert calculate_period([1, 2, 3, 4, 5]) == 5
    # Test with immediate repetition
    assert calculate_period([1, 1, 2, 3]) == 1


def test_gcd():
    assert gcd(48, 18) == 6
    assert gcd(54, 24) == 6
    assert gcd(7, 13) == 1
    assert gcd(0, 5) == 5
    assert gcd(5, 0) == 5


def test_estimate_pi():
    # Test with coprime numbers
    sequence = [2, 3, 4, 7, 5, 11]
    estimated_pi = estimate_pi(sequence)
    assert isinstance(estimated_pi, float)

    # Test with insufficient numbers
    assert estimate_pi([1]) == "Not enough random numbers to estimate."

    # Test with non-coprime numbers
    sequence = [2, 4, 6, 8, 10, 12]
    assert estimate_pi(sequence) == float('inf')


def test_generate_system_sequence():
    sequence = generate_system_sequence(10)
    assert len(sequence) == 10
    assert all(isinstance(x, int) for x in sequence)
    assert all(7 ** 3 + 89 <= x <= 2 ** 20 - 1 for x in sequence)