# Problem 32 — Pandigital Products

## Problem

We shall say that an $n$-digit number is **pandigital** if it makes use of all the digits $1$ to $n$ exactly once. For example, the 5-digit number, $15234$, is $1$ through $5$ pandigital.

The product $7254$ is unusual, as the identity, $39 \times 186 = 7254$, containing multiplicand, multiplier, and product is $1$ through $9$ pandigital.

**Find the sum of all products whose multiplicand/multiplier/product identity can be written as a $1$ through $9$ pandigital.**

> HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.

A "way" is an identity `(A, B, P)` such that `A × B = P` and the concatenation of the digits of `A`, `B`, and `P` uses each digit from `1` to `9` exactly once. The order of multiplicand and multiplier does not matter (`A × B` is the same identity as `B × A`). Each distinct product `P` is counted only once in the final sum, regardless of how many valid identities produce it.

## Understanding the problem

This is a **digit-constrained enumeration** problem: we are searching for identities of the form `A × B = P` where the three numbers together use every digit from 1 through 9 exactly once.

Key observations:

- Digits used: exactly `{1, 2, 3, 4, 5, 6, 7, 8, 9}` — no zeros allowed.
- Total digits: $a + b + p = 9$, where `a`, `b`, `p` are the number of digits in A, B, and P respectively.
- Since $P = A × B$, the number of digits in P is determined by the size of A and B, which constrains which digit-length splits are possible.

### Valid digit-length splits

For `A` with `a` digits and `B` with `b` digits, their product `P` can have at most `a + b` digits (roughly). We need exactly 9 total:

| Split `(a, b)` | Product P must have | Is it valid? |
|-----------------|---------------------|--------------|
| `(1, 4)`       | $9 - 1 - 4 = 4$ digits | Yes (e.g., `9 × 1234` can be 4-digit product) |
| `(2, 3)`       | $9 - 2 - 3 = 4$ digits | Yes (e.g., `99 × 999` can be 5 digits, but 4-digit products are possible for smaller values) |
| `(1, 3)`       | $9 - 1 - 3 = 5$ digits | No — product of a 1-digit and 3-digit number is at most 4 digits (9 × 999 = 8991). |
| `(3, 3)`       | $9 - 3 - 3 = 3$ digits | No — smallest 3-digit numbers multiply to at least $100 × 100 = 10000$ (5 digits). |
| `(1, 5)`       | $9 - 1 - 5 = 3$ digits | No — $9 × 99999 = 899991$ (6 digits minimum product for 1×5). |

So the **only** valid splits are:
- `(1, 4, 4)`: A has 1 digit, B has 4 digits, P has 4 digits
- `(2, 3, 4)`: A has 2 digits, B has 3 digits, P has 4 digits

### Range constraints

For the split `(a, b) = (1, 4)`:
- A ∈ [1, 9]
- B ∈ [1023, 9876] (roughly; must have 4 distinct non-zero digits)
- P ∈ [1234, 9876]

For the split `(a, b) = (2, 3)` with `a + b = 5`:
- A ∈ [12, 98]
- B ∈ [123, 987]
- P must be 4 digits: $P = A × B < 10000$, so we need $A × B ≤ 9999$

## Ways to solve it

### 1. Brute-force enumeration over valid splits — straightforward and efficient enough

Iterate over all possible (A, B) pairs for both valid digit-length splits `(1,4)` and `(2,3)`, check if the concatenated string `str(A) + str(B) + str(P)` is pandigital using a set or sorted comparison against `"123456789"`.

```text
pandigital_products = set()

// Split (1, 4): A has 1 digit, B has 4 digits
for A from 1 to 9:
    for B from 1023 to 9876:
        P = A * B
        if str(A) + str(B) + str(P) is pandigital with 9 distinct non-zero digits:
            pandigital_products.add(P)

// Split (2, 3): A has 2 digits, B has 3 digits
for A from 12 to 98:
    for B from 123 to min(987, floor(9999 / A)):
        P = A * B
        if str(A) + str(B) + str(P) is pandigital with 9 distinct non-zero digits:
            pandigital_products.add(P)

answer = sum(pandigital_products)
```

An important optimization: for the `(2,3)` split we only need to iterate A up to $9876$ (since $12345 / 9 \approx 1371$), but more tightly A ≤ 99 and B ≤ 999. Combined with `P = A × B < 10000`, we can restrict B's upper bound to `floor(9999 / A)`.

Total iterations:
- `(1,4)` split: $9 × 8854 ≈ 79,686$
- `(2,3)` split: at most $87 × 865 ≈ 75,255$ (loose bound; tighter with the floor constraint)

This is well under 200K iterations — instantaneous for any language.

### 2. Digit-based permutation approach — enumerate pandigital strings directly

Generate all permutations of `"123456789"`, split each permutation into `(A, B)` according to both valid splits, compute `P = A × B`, and check if P uses the remaining digits.

```text
pandigital_products = set()

for each permutation of "123456789":
    // Try split (1, 4): first digit = A, next 4 digits = B
    A = int(perm[0])
    B = int(perm[1:5])
    P = A * B
    P_str = str(P)
    if len(P_str) == 4 and set(P_str) uses remaining 4 digits perm[5:9]:
        pandigital_products.add(P)

    // Try split (2, 3): first 2 digits = A, next 3 digits = B
    A = int(perm[0:2])
    B = int(perm[2:5])
    P = A * B
    P_str = str(P)
    if len(P_str) == 4 and set(P_str) uses remaining 4 digits perm[5:9]:
        pandigital_products.add(P)

answer = sum(pandigital_products)
```

- Number of permutations: $9! = 362{,}880$ — small enough.
- Each permutation checks against both splits → ~725K digit-set comparisons total.
- The set ensures no product is counted twice (some may be found via different splits/permutations).

### 3. Backtracking with pruning — reduce the search space intelligently

Build digits of A, B from left to right, maintaining a bitmask of used digits. At each step, prune branches where:
- The current partial A or B would exceed its target digit count.
- The product P cannot possibly have the correct length (using lower/upper bounds on remaining values).

```text
function backtrack(used_mask, pos_in_concatenation):
    // pos tracks how many digits we've placed so far.
    // Place next digit for either A, B, or determine when to compute P.

    if 4 digits placed in concatenation (A and B complete):
        P = current_A * current_B
        check if P uses exactly the remaining 5 unused digits (9 - used_digit_bitmask)
        add P if valid
        return

    for d from 1 to 9:
        if d not in used_mask:
            backtrack(used_mask | (1 << d), pos + 1)
```

With pruning this is significantly faster than the permutation approach because we never complete an invalid partial identity. The bitmask `used_mask` tracks which digits are consumed by the parts of A and B placed so far, and the product is only checked at the leaf.

### 4. Set/bitmask optimization — fast pandigital checking

Instead of string comparisons, use bitmasks for digit presence:

```text
function is_pandigital_9(A, B, P):
    mask = countSetBits(A) | countSetBits(B) | countSetBits(P)
    return mask == 0x1FF and no zeros and no repeated digits
```

Where `countSetBits(n)` produces a bitmask with bit i set if digit i appears in n's decimal representation, and the "no zeros" / "no repeats" checks are done alongside. This avoids any string conversion overhead entirely.

## Recommended approach

- **For clarity and simplicity**: use approach **1** (brute-force enumeration). It is trivially implementable (~40 lines), runs in well under a millisecond, and is easy to verify by hand. The iteration counts are small enough that brute force is not just practical but optimal for this problem's scale.
- **For elegance**: use approach **2** (permutation-based) if you want a concise implementation using a built-in permutation library — the total work is comparable.
- **Approach 3** (backtracking with pruning) is ideal if you expect larger constraints and want to demonstrate optimization skills. It reduces redundant computation by pruning invalid partial identities early.
- **Approach 4** (bitmask optimization) is a useful optimization layer that can be mixed into any of the above approaches for faster digit validation without string allocations.

## Verification

The final answer for this problem must be:

> **45228**

Any other value means a bug. Common mistakes:
- Counting duplicate products (failing to deduplicate), which inflates the sum.
- Including zeros in pandigital checks — the problem specifies digits 1–9 only, no 0.
- Missing one of the splits `(1,4)` or `(2,3)` during enumeration.
