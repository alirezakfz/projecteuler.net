# Problem 33 — Digit Cancelling Fractions

## Problem

The fraction $49/98$ is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that $49/98 = 4/8$, which is correct, is obtained by cancelling the $9$s.

We shall consider fractions like, $30/50 = 3/5$, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the denominator.

## Understanding the problem

This is a **digit manipulation + enumeration** problem: we are looking for 2-digit/2-digit fractions where cancelling one common digit (incorrectly) produces an equivalent simplified fraction.

Key constraints:

- Both numerator and denominator have exactly **2 digits**.
- The fraction value is **less than 1** (numerator < denominator).
- There is at least one **common non-zero digit** in the numerator's two digits and the denominator's two digits.
- Cancelling that shared digit must produce a **correctly equivalent** smaller fraction.
- Exclude **trivial examples**: fractions where the cancelled digit is `0` (e.g., `30/50 = 3/5`).

So the task boils down to: iterate all valid 2-digit-by-2-digit fractions, try cancelling each shared non-zero digit, check if the resulting fraction equals the original, collect those that do. The product of these four weird fractions (in unreduced form) is then simplified to lowest terms — report just the denominator.

## Ways to solve it

### 1. Direct brute-force enumeration — simplest and most efficient

Iterate all possible numerators `n` from 11–98 and denominators `d` from `n+1`–99 (ensuring fraction < 1). For each pair, extract their digits:

```
n = ones(n) * 10 + tens(n)    # i.e. n_digits[0]*10 + n_digits[1]
d = ones(d) * 10 + tens(d)
```

Check for shared non-zero digits between `{n_digits[0], n_digits[1]}` and `{d_digits[0], d_digits[1]}`. For each common digit `c`:

```
# Cancel c from numerator and denominator (remove first occurrence)
n_canc  = fraction with digit c removed from n's 2 digits → 1-digit result
d_canc  = fraction with digit c removed from d's 2 digits → 1-digit result

# Check: does n/d == n_canc/d_canc ?
equivalent = (n * d_canc == d * n_canc)   # cross-multiply to avoid floating point
```

If equivalent and `c != 0`, add `(n, d)` to the list of curious fractions.

Collect all four, compute their product as unreduced fractions:

```
numerator_product = n1 * n2 * n3 * n4
denominator_product = d1 * d2 * d3 * d4
```

Reduce by dividing both by `gcd(numerator_product, denominator_product)`, then return the reduced denominator.

- Search space: ~90 × 90 ≈ **8,100** pairs — trivially fast.
- Total complexity: < 10K operations.

### 2. Digit-position-based enumeration — structured approach

Instead of checking all (n, d) and extracting digits, enumerate by digit position directly:

```text
For each common digit c from 1 to 9:
    For each cancellation type:
        Type ab/cb → cancel b: fractions a/c = ab/cb   (cancel units digit of both)
        Type ab/ca → cancel a: fractions b/c = ab/ca   (cancel tens digit of both)
        Type ac/bc → cancel c: fractions a/b = ac/bc   (cancel units digit shared)
        Type ca/cb → cancel c: fractions a/b = ca/cb   (cancel tens digit shared)

For each type, iterate the remaining free digits and verify that ab/cb actually equals a/c
(using cross-multiplication to avoid float issues).
```

This enumerates by structure rather than brute-force — same result but more organized. There are **4 cancellation patterns** (left/right on top/bottom) × 9 possible common digits = 36 structural templates, each with ~81 digit combinations still needing verification.

### 3. Equation-based approach — fewer candidates via algebra

For the case where we cancel the units digit: `ab/cb = a/c` becomes `(10a + b)/(10c + b) = a/c`. Cross-multiplying:

```
c(10a + b) = a(10c + b)
10ac + bc = 10ac + ab
bc = ab    →   c = a (if b != 0... but that would make n=d, excluded)

Wait — more carefully:
(10n1 + n2) / (10d1 + d2) = n_reduced / d_reduced
```

This approach derives constraints algebraically. For example, when `ab/cb` type cancels common units digit `b`:

```
(10·p + b) / (10·q + b) = p/q    →   q(10p+b) = p(10q+b) → qb + pb = pb → wait, this always holds? No...

Actually:  n/d = n_canc/d_canc
n_canc and d_canc are 1-digit numbers obtained by removing common digit.

So we just solve the equation for given structure rather than enumerate — but with only 2 digits each, enumeration is simpler and equally fast.
```

Algebraic constraints help verify correctness (the answer should be a small integer) but don't substantially reduce work at this scale.

## Recommended approach

- **Use approach 1** (direct brute-force). With ~8K pairs to check, no optimization is needed. The implementation is ~20 lines and directly mirrors the problem statement.
- Use **cross-multiplication** (`n × d_canc == d × n_canc`) to verify equivalence — avoids all floating-point precision issues.

## Verification

The known final answer (the reduced denominator) is:

> **100**

Any other value means a bug. Common mistakes:
- Including trivial zero-cancelling fractions (like 30/50).
- Using floating-point comparison instead of cross-multiplication, which causes subtle errors near equivalent ratios.
- Not reducing the final product to lowest terms before extracting the denominator.
