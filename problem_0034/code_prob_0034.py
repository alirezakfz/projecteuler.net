"""
Problem 34 — Digit Factorials
Find the sum of all numbers equal to the sum of the factorial of their digits.
Excluding 1 and 2 (not sums). Expected answer: 40730
"""

from itertools import combinations_with_replacement


# Precomputed digit factorials: 0! through 9!
FACTORIALS = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]


def _digit_factorial_sum(n):
    """Compute sum of factorial of each digit in n."""
    return sum(FACTORIALS[int(digit)] for digit in str(n))


# ---------------------------------------------------------------------------
# Approach 1: Direct brute-force enumeration with proven upper bound
# ---------------------------------------------------------------------------

def solution_brute_force():
    """Approach 1: check every number up to the proven bound (~2.4M+)."""
    UPPER_BOUND = 362880 * 7  # max possible factorial sum for 7 digits
    curious_numbers = []

    for n in range(3, UPPER_BOUND + 1):
        if _digit_factorial_sum(n) == n:
            curious_numbers.append(n)

    total = sum(curious_numbers)
    print(f"Approach 1 (Brute-force): found {len(curious_numbers)} numbers: {curious_numbers}")
    print(f"Answer (sum): {total}")
    return total, list(curious_numbers)


# ---------------------------------------------------------------------------
# Approach 2: Multiset enumeration — enumerate digit multisets directly
# ---------------------------------------------------------------------------

def solution_multisets():
    """Approach 2: enumerate digit multisets whose factorial sum matches digits."""
    curious_numbers = set()

    for num_digits in range(1, 8):
        min_val = 10 ** (num_digits - 1) if num_digits > 1 else 3

        for multiset in combinations_with_replacement(range(10), num_digits):
            fact_sum = sum(FACTORIALS[d] for d in multiset)

            s = str(fact_sum)
            if len(s) != num_digits:
                continue

            if fact_sum < min_val:
                continue

            if tuple(sorted(int(ch) for ch in s)) == multiset:
                curious_numbers.add(fact_sum)

    result = sorted(c for c in curious_numbers if c >= 3)
    total = sum(result)
    print(f"\nApproach 2 (Digit multisets): found {len(result)} numbers: {result}")
    print(f"Answer (sum): {total}")
    return total, result


if __name__ == "__main__":
    import time

    approaches = [
        ("Brute-force", solution_brute_force),
        ("Digit multisets", solution_multisets),
    ]

    results = []
    for name, func in approaches:
        t0 = time.perf_counter()
        total, nums = func()
        elapsed = (time.perf_counter() - t0) * 1000
        results.append((name, total))
        print(f"Time: {elapsed:.3f}ms")

    totals = set(r[1] for r in results)
    if len(totals) == 1:
        print(f"\nAll approaches agree: answer = {totals.pop()}")
    else:
        print(f"\nMISMATCH! Results: {set(r[1] for r in results)}")
