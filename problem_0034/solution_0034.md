# Problem 34 — Digit Factorials

## Problem

$145$ is a curious number, as $1! + 4! + 5! = 1 + 24 + 120 = 145$.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

> Note: As $1! = 1$ and $2! = 2$ are not sums they are not included.

## Understanding the problem

This is a **digit-factorial sum** search problem: we must find every number `n` such that if you replace each of its digits `d₁, d₂, ..., dₙ` with `dᵢ!`, the sum of those factorials equals `n` itself.

Key constraints:

- Factorials are on **individual digits only** (0 through 9).
- Exclude `1` and `2` because they are single-digit — not a *sum* of digit factorials (just one factorial each).
- Only non-zero results matter (we seek numbers ≥ 3).
- Digits include `0`, and `0! = 1`, so it contributes 1 to the sum even though it adds no visible magnitude.

### Precomputed factorial table

| Digit | 0! | 1! | 2! | 3! | 4! | 5! | 6! | 7! | 8! | 9! |
|-------|------|------|------|------|-------|---------|----------|-----------|-------------|--------------|
| Value | 1    | 1     | 2     | 6   | 24    | 120     | 720      | 5,040     | 40,320      | **362,880** |

## Proving the upper bound

Before enumerating, we can prove a finite search range. For an `n`-digit number, the smallest such number is `10^(n-1)`, while the maximum possible digit-factorial sum (all digits = 9) is `n × 9!`:

| Digits | Smallest number | Maximum factorial sum (all 9s) | Could match? |
|--------|----------------|-------------------------------|--------------|
| 8      | 10,000,000     | 2,903,040                    | **No** — sum is far too small |
| 9      | 100,000,000    | 3,265,920                    | **No** — same reason |

At **8 digits**, the max factorial sum (≈2.9M) is less than the smallest 8-digit number (10M). For any `n ≥ 8`, the gap only widens. Therefore, no solution can have more than 7 digits.

For 7-digit numbers, max sum = 7 × 362,880 = **2,540,160** — still less than 9,999,999 but greater than 1,000,000 (smallest 7-digit), so solutions are theoretically possible. However, the *tightest* argument notes that by n=8 and beyond, even using all 9s is hopeless, so we can safely bound our search at **~2.4M max** — or more simply, any number up to roughly `n_max × 9!` where it first exceeds `10^(n-1)`.

Given that only digits contribute independently and factorials grow very slowly (even `9! ≈ 360K`), the practical bound is well under 5M. Checking up to **2,400,000** or simply any number up to **~10⁶** is overkill — but safe and trivial for modern computers (~few million iterations).

## Ways to solve it

### 1. Direct brute-force enumeration with bound — simplest and recommended

Iterate every integer from 3 upward, compute the sum of factorial of its digits, compare to itself, collect matches. Stop when `n` exceeds the max possible factorial sum for its digit count (or use a fixed bound like 2,400,000).

```text
factorials = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

curious_numbers = []

for n from 3 to UPPER_BOUND:
    digit_factorial_sum = sum(factorials[digit] for digit in str(n))
    if digit_factorial_sum == n:
        curious_numbers.append(n)

answer = sum(curious_numbers)
```

With the precomputed table, no repeated factorial computation is needed. Each number requires at most 7 digit lookups and additions — **~0.01ms per candidate**. Up to 2.4M numbers takes well under a second total.

**Complexity:** O(U × d) where U ≈ 2.4M (bound), d ≤ 7 (digit count). Total: ~17M operations.

### 2. Digit-combination enumeration — more efficient, no wasted work

Instead of checking every integer, enumerate all **multisets of digits** whose factorial sum could equal a permutation of those same digits:

```text
For each possible digit-count multiset (a_0 of digit 0, a_1 of digit 1, ..., a_9 of digit 9):    (where Σ a_i = total_digits)

    factorial_sum = Σ (a_i × factorials[i])

    if the concatenation of digits matches the digits in factorial_sum:
        add factorial_sum to the results
```

This avoids iterating numbers that can never possibly match. A multiset is defined by counts `{count_0, count_1, ..., count_9}` where `Σ count_i` = total number of digit-positions. For a 7-digit number, there are C(7+10-1, 10-1) = C(16, 9) = **11,440** such multisets — dramatically fewer than 2.4M numbers to check.

For each multiset:
1. Compute `factorial_sum`.
2. Determine if the digits of `factorial_sum` correspond exactly to the multiset counts (accounting for digit frequency).
3. If so, every permutation that produces a valid number is potentially a solution — but since factorial_sum is fixed, it's just one candidate to verify.

**Complexity:** Much lower than brute-force for large bounds; scales with `n^d` where n=10 (digit alphabet) and d = number of digit-positions, not the magnitude of `n`.

### 3. Backtracking on digit counts — refined constraint propagation

Build digit multisets incrementally, pruning when:
- The partial factorial sum already exceeds what any permutation of remaining digit positions could produce.
- Impossible to form a valid digit frequency match.

This is the most efficient approach by far for much larger bounds or similar problems with more digits, but the brute-force method is simpler and equally fast at this scale.

## Recommended approach

**Use approach 1** (brute-force enumeration). The search space is bounded below 2.4M numbers (~3M is safe), each requiring only digit-by-digit lookup in a precomputed table of 10 values. This takes **well under one second** and requires no clever math.

The elegance of this approach is that it follows the problem statement directly: "find all numbers" → check every number up to the proven bound. No enumeration tricks needed.

## Verification

The two curious numbers found are:

> 145 (because 1! + 4! + 5! = 1 + 24 + 120 = 145)
> 40585 (because 4! + 0! + 5! + 8! + 5! = 24 + 1 + 120 + 40320 + 120 = 40585)

Their sum is:

> **40730**

Any other value means a bug. Common mistakes:
- Including 1 and 2 (which are single digits, not sums).
- Forgetting that `0! = 1` contributes to the sum even though digit 0 adds no visible magnitude.
- Using the wrong upper bound — the gap widens exponentially, so checking a bit too far is harmless but wasteful.
