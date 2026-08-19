"""Project Euler 31 - Coin Sums.

Count the number of ways to make £2 (200p) using the eight UK coins:
1p, 2p, 5p, 10p, 20p, 50p, 100p, 200p.
Known answer: 73682.
"""

from functools import lru_cache

COINS = [1, 2, 5, 10, 20, 50, 100, 200]
TARGET = 200
EXPECTED = 73682


def dp_coin_change(coins=COINS, target=TARGET):
    """Approach 1: bottom-up dynamic programming (combinations)."""
    ways = [0] * (target + 1)
    ways[0] = 1
    for c in coins:
        for a in range(c, target + 1):
            ways[a] += ways[a - c]
    return ways[target]


def memoize_coin_change(coins=COINS, target=TARGET):
    """Approach 2: top-down recursion with memoization."""

    @lru_cache(maxsize=None)
    def count(prefix, remaining):
        if remaining == 0:
            return 1
        if prefix == len(coins):
            return 0
        skip = count(prefix + 1, remaining)
        c = coins[prefix]
        use = count(prefix, remaining - c) if remaining >= c else 0
        return skip + use

    count.cache_clear()
    return count(0, target)


def brute_force(target=TARGET):
    """Approach 3: brute-force nested loops, one per denomination.

    Six nested loops fix the counts of 200p/100p/50p/20p/10p/5p; the remaining
    amount is then split between 2p and 1p, and the number of ways to do that
    is (r // 2) + 1 (choosing how many 2p coins, the rest forced to 1p).
    """
    count = 0
    for n200 in range(target // 200 + 1):
        for n100 in range((target - 200 * n200) // 100 + 1):
            for n50 in range((target - 200 * n200 - 100 * n100) // 50 + 1):
                for n20 in range((target - 200 * n200 - 100 * n100 - 50 * n50) // 20 + 1):
                    for n10 in range((target - 200 * n200 - 100 * n100 - 50 * n50 - 20 * n20) // 10 + 1):
                        for n5 in range((target - 200 * n200 - 100 * n100 - 50 * n50 - 20 * n20 - 10 * n10) // 5 + 1):
                            r = target - 200 * n200 - 100 * n100 - 50 * n50 - 20 * n20 - 10 * n10 - 5 * n5
                            count += r // 2 + 1
    return count


def generating_function(coins=COINS, target=TARGET):
    """Approach 4: coefficient of x^target in the product of series.

    For each coin of value d the series 1/(1 - x^d) has coefficients all 1;
    multiply the series (truncated at `target`) and take coefficient target.
    """
    poly = [0] * (target + 1)
    poly[0] = 1
    for c in coins:
        next_poly = [0] * (target + 1)
        for a in range(target + 1):
            if poly[a]:
                n = a
                while n <= target:
                    next_poly[n] += poly[a]
                    n += c
        poly = next_poly
    return poly[target]


def main():
    results = {
        "1. Bottom-up DP": dp_coin_change(),
        "2. Top-down memoized": memoize_coin_change(),
        "3. Brute-force loops": brute_force(),
        "4. Generating function": generating_function(),
    }
    all_ok = True
    for name, value in results.items():
        ok = value == EXPECTED
        all_ok &= ok
        print(f"{name}: {value:>10}  {'OK' if ok else 'FAIL (expected ' + str(EXPECTED) + ')'}")
    print("\nAll approaches agree:", all_ok)
    return all_ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
