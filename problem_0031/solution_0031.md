# Problem 31 — Coin Sums

## Problem

In the United Kingdom the currency is made up of pound (£) and pence (p).
There are eight coins in general circulation:

> 1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).

How many different ways can £2 (i.e. 200p) be made using any number of coins?

A "way" is a **multiset** of coins — the *order* in which coins are laid out
does not matter (e.g. `20p + 10p` is the same combination as `10p + 20p`).

## Understanding the problem

This is a classic **coin-change counting** problem: given a set of coin
denominations, count the number of combinations — using unlimited copies of
each coin — that sum to a target amount (200p).

Key observations:

- Coins are **unlimited**: any combination may use any number of each coin.
- Order does **not** matter: we only count distinct multisets of coins.
- A small combinatorial search space, but naive enumeration explodes
  quickly, so a counting technique is needed.

The known answer is **73682** (a good sanity-check for any implementation).

## Ways to solve it

### 1. Dynamic programming (bottom-up) — the standard/efficient approach

Define `ways[amount][i]` = number of ways to make `amount` pence using only
the first `i` denominations. Build a 1-D or 2-D table:

- `ways[0] = 1` (one way to make 0p: use no coins).
- For each coin `c` (outer loop), for each amount `a` from `c` up to 200
  (inner loop): add `ways[a - c]` into `ways[a]`.

The order of loops matters: iterating **coins on the outside, amounts on the
inside** makes each coin type usable any number of times while *preventing*
permutations of the same multiset from being counted multiple times.

```text
coins  = [1, 2, 5, 10, 20, 50, 100, 200]
ways[0] = 1
for c in coins:
    for a in range(c, 201):
        ways[a] += ways[a - c]
answer = ways[200]
```

- Time complexity: `O(len(coins) * target)` here `target = 200`, so `O(8 * 200)`.
- Scales cleanly to larger targets (larger values of `target`) with no
  change to the algorithm.

### 2. Recursion with memoization (top-down DP)

Count combinations as a recursion:

```
count(prefix, remaining):
    # prefix = index into the denominations list (how many denominations
    #       we have considered so far)
    if remaining == 0:       return 1
    if prefix == len(coins): return 0
    # Either skip this denomination entirely, or use it (and allow reuse),
    # so each multiset is reached exactly once.
    skip = count(prefix + 1, remaining)
    use  = (remaining >= coins[prefix]) ? count(prefix, remaining - coins[prefix]) : 0
    return skip + use
```

Memoize on `(prefix, remaining)`.

The key trick is that `use` calls `count(prefix, remaining - coins[prefix])`
with the **same** `prefix`, which allows the current denomination to be
reused, while `skip` advances to the next denomination. This is exactly the
bottom-up DP of approach 1 written top-down — so it yields the same answer
(73682), and is often the clearest to reason about.

### 3. Brute-force nested loops (enumeration) — works but inefficient

Eight nested loops, one per denomination, with a constraint that the loops'
counts are non-increasing in "coin index" to enforce that order is ignored:

```
for c1 in range(0..200//200):          # £2
  for c2 in ...:                       # £1
    for c3 in ...:                     # 50p
      ...
        if remaining == 0: count += 1
```

Simple and correct, but:

- Worst-case iteration count is on the order of `O(target^n)` in the number of
  denominations `n` and grows super-linearly with `target` — fine at 200p, but
- Does not scale to larger targets or more denominations,
- Hard to generalize or maintain (requires exactly one loop per denomination).

Useful only to *verify* the DP result by hand.

### 4. Generating functions (mathematical/formal)

The number of ways to make 200p is the coefficient of `x^200` in the
**product** of the generating functions for each coin:

```
P(x) = 1/(1 - x)        · 1/(1 - x^2)
     × 1/(1 - x^5)      · 1/(1 - x^10)
     × 1/(1 - x^20)     · 1/(1 - x^50)
     × 1/(1 - x^100)    · 1/(1 - x^200)
```

Computing that coefficient by hand is infeasible, but this formulation is
useful for deriving DP recurrences, or for symbolic/combinatorial analysis.

## Recommended approach

- **For a correct, readable, scalable implementation**: use approach **1**
  (bottom-up DP) — it is ~10 lines, trivially fast, and generalizes to any
  target amount.
- **Approach 2** is preferred if you want a top-down "readable" version with
  memoization.
- **Approach 3** and **4** are useful for verification and mathematical
  understanding, but not for a real solution.

## Verification

Whatever method is used, the final answer for 200p must be:

> **73682**

Any other value means a bug (most commonly: counting permutations instead of
combinations, i.e. wrong loop order in the DP, or off-by-one in a range).
