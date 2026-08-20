"""
Problem 33 — Digit Cancelling Fractions
Find the denominator of the product of four non-trivial curious fractions
(2-digit numerator, 2-digit denominator, < 1) where cancelling one common
non-zero digit produces an equivalent fraction.
Expected answer: 100
"""

from math import gcd
from functools import reduce


def _digits(n):
    """Return the two digits of a 2-digit number as (tens, units)."""
    return (n // 10, n % 10)


def _is_curious(numerator, denominator):
    """Check if cancelling a shared non-zero digit between numerator and
    denominator yields an equivalent fraction. Returns the reduced fraction
    (reduced_n, reduced_d) if curious, or None."""

    # Skip trivial: cancelled digit is 0
    n_digits = _digits(numerator)
    d_digits = _digits(denominator)

    results = []

    # Try cancelling each shared non-zero digit
    for nd in n_digits:
        if nd == 0:
            continue
        if nd in d_digits:
            # Remove first occurrence from numerator and denominator
            num_list = list(n_digits)
            den_list = list(d_digits)
            num_list.remove(nd)
            den_list.remove(nd)
            reduced_n = num_list[0]
            reduced_d = den_list[0]

            if reduced_d == 0:
                continue

            # Cross-multiply to avoid float issues
            if numerator * reduced_d == denominator * reduced_n:
                results.append((reduced_n, reduced_d))

    return results


def solution_curious_fractions():
    """Find all curious fractions, compute their product, return reduced denominator."""
    curious = []

    for n in range(10, 99):          # numerator: 2-digit
        for d in range(n + 1, 100):  # denominator > numerator (fraction < 1), 2-digit
            result = _is_curious(n, d)
            if result:
                curious.append((n, d))

    print(f"Found {len(curious)} curious fractions:")
    for n, d in curious:
        print(f"  {n}/{d}")

    # Compute the product of all four fractions (unreduced)
    numerator_product = reduce(lambda a, b: a * b, (c[0] for c in curious))
    denominator_product = reduce(lambda a, b: a * b, (c[1] for c in curious))

    common = gcd(numerator_product, denominator_product)
    reduced_numerator = numerator_product // common
    reduced_denominator = denominator_product // common

    print(f"\nProduct (unreduced): {numerator_product}/{denominator_product}")
    print(f"Product (reduced):   {reduced_numerator}/{reduced_denominator}")
    print(f"Answer (denominator): {reduced_denominator}")

    return reduced_denominator, curious


def solution_brute_force():
    """Alternative: verify by iterating all pairs structurally."""
    curious = []

    for n in range(10, 99):
        for d in range(n + 1, 100):
            nd = _digits(n)
            dd = _digits(d)

            # All possible cancellation positions (digit index in num, digit index in den)
            for ni in range(2):
                for di in range(2):
                    if nd[ni] == 0 or nd[ni] != dd[di]:
                        continue

                    # Remove matching digit from both
                    reduced_n = (nd[1 - ni]) if ni == 0 else (nd[0])
                    reduced_d = (dd[1 - di]) if di == 0 else (dd[0])

                    if reduced_d == 0:
                        continue

                    if n * reduced_d == d * reduced_n:
                        curious.append((n, d))
                        break
                else:
                    continue
                break

    # Deduplicate by fraction value
    unique = list({(n, d) for n, d in curious})
    print(f"\nBrute-force verification: {len(unique)} fractions found")

    numerator_product = reduce(lambda a, b: a * b, (f[0] for f in unique))
    denominator_product = reduce(lambda a, b: a * b, (f[1] for f in unique))
    common = gcd(numerator_product, denominator_product)
    final_denom = denominator_product // common
    print(f"Reduced denominator: {final_denom}")


if __name__ == "__main__":
    solution_curious_fractions()
    print()
    solution_brute_force()
