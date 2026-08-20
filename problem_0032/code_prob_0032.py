"""
Problem 32 — Pandigital Products
Find the sum of all products whose multiplicand/multiplier/product identity
can be written as a 1-through-9 pandigital.
Expected answer: 45228
"""

from itertools import permutations


# ---------------------------------------------------------------------------
# Approach 1: Brute-force enumeration over valid digit-length splits
# ---------------------------------------------------------------------------

def _is_pandigital_1_to_n(s, n):
    """Check if string s contains digits 1..n exactly once."""
    return len(s) == n and sorted(s) == [str(d) for d in range(1, n + 1)]


def solution_brute_force():
    """Approach 1: enumerate (A,B) pairs for splits (1,4) and (2,3)."""
    pandigital_products = set()

    # Split (1, 4): A is 1-digit, B is 4-digit, P should be 4-digit
    for a in range(1, 10):
        for b in range(1023, 9877):
            p = a * b
            if p > 9999:
                continue
            s = f"{a}{b}{p}"
            if len(s) == 9 and _is_pandigital_1_to_n(s, 9):
                pandigital_products.add(p)

    # Split (2, 3): A is 2-digit, B is 3-digit, P should be 4-digit
    for a in range(12, 99):
        for b in range(123, min(988, 10000 // a + 1)):
            p = a * b
            if p > 9999:
                continue
            s = f"{a}{b}{p}"
            if len(s) == 9 and _is_pandigital_1_to_n(s, 9):
                pandigital_products.add(p)

    return sum(pandigital_products), pandigital_products


# ---------------------------------------------------------------------------
# Approach 2: Permutation-based — enumerate all permutations of "123456789"
# ---------------------------------------------------------------------------

def solution_permutation():
    """Approach 2: iterate perms, split into (A,B), check product."""
    pandigital_products = set()

    for perm in permutations("123456789"):
        s = "".join(perm)  # full 9-digit pandigital string

        # Try split (1, 4): A=1 digit, B=4 digits, remaining 4 = P
        a = int(s[0])
        b = int(s[1:5])
        p = a * b
        if p == int(s[5:9]):
            pandigital_products.add(p)

        # Try split (2, 3): A=2 digits, B=3 digits, remaining 4 = P
        a = int(s[0:2])
        b = int(s[2:5])
        p = a * b
        if p == int(s[5:9]):
            pandigital_products.add(p)

    return sum(pandigital_products), pandigital_products


# ---------------------------------------------------------------------------
# Approach 3: Backtracking with bitmask pruning
# ---------------------------------------------------------------------------

def _count_set_bits(n):
    """Count number of set bits (population count)."""
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def _to_digit_mask(n):
    """Return a bitmask where bit i is set if digit i appears in n.
    Also detects zeros or repeated digits."""
    mask = 0
    while n > 0:
        d = n % 10
        if d == 0:
            return -1  # zero not allowed
        if mask & (1 << d):
            return -2   # repeated digit
        mask |= 1 << d
        n //= 10
    return mask


def _check_pandigital_bitmask(a, b, p):
    """Check if A+B+P together form pandigital 1..9 using bitmasks."""
    mask_a = _to_digit_mask(a)
    if mask_a < 0:
        return False
    mask_b = _to_digit_mask(b)
    if mask_b < 0 or (mask_a & mask_b):
        return False
    mask_p = _to_digit_mask(p)
    if mask_p < 0 or (mask_p & (mask_a | mask_b)):
        return False
    combined = mask_a | mask_b | mask_p
    return combined == 0x1FF  # bits 1-9 all set


def solution_backtracking():
    """Approach 3: backtracking build A and B digit by digit."""
    pandigital_products = set()

    def _try_assign(placed, a_partial, b_partial):
        """
        placed: bitmask of digits used in A and B so far.
        a_partial, b_partial: current values being built (None if not started).
        We place digits for concatenation A+B (A first, then B),
        then check the product at completion.
        Position in concatenated A+B: 0..3 (split 1|4) or 0..4 (split 2|3).
        """
        if placed == 0xF9E:  # all 5 digit-positions of A+B filled (we track count via a_partial/b_partial length)
            pass

        # Instead, use explicit depth-based recursion for clarity
        return

    def _backtrack_ab(depth, used_mask, a_val, b_val):
        """Build digits of A+B from left to right (a_val = A so far, b_val = B so far)."""
        if depth > 0 and a_val == 0:
            return  # leading zero not possible since we use 1..9

        # Check if A (first part) is complete based on split
        # For split (1,4): after placing 1 digit, A is done; B gets next 4
        # For split (2,3): after placing 2 digits, A is done; B gets next 3

        # Try both splits by checking at each depth if A can be finalized
        for split_a_len in (1, 2):
            if depth < split_a_len:
                continue  # not enough digits placed yet to finalize A

            # At this depth, A is complete with the first `split_a_len` digits
            # But we need to actually extract the correct A and B from our construction.
            # Simpler: use fixed-length construction for each split at top level.
            pass

    def _backtrack_split_one_four():
        """Build A (1 digit) + B (4 digits) via recursion over used-mask."""
        results = set()

        def _build(pos, used_mask, b_val):
            if pos == 5:
                p = a_singleton * b_val
                if _check_pandigital_bitmask(a_singleton, b_val, p):
                    results.add(p)
                return
            for d in range(1, 10):
                if used_mask & (1 << d):
                    continue
                _build(pos + 1, used_mask | (1 << d), b_val * 10 + d)

        for a_singleton in range(1, 10):
            _build(1, 1 << a_singleton, 0)
        return results

    def _backtrack_split_two_three():
        """Build A (2 digits) + B (3 digits) via recursion over used-mask."""
        results = set()

        def _build(pos, used_mask, a_val, b_val):
            if pos == 5:
                p = a_val * b_val
                if _check_pandigital_bitmask(a_val, b_val, p):
                    results.add(p)
                return
            for d in range(1, 10):
                if used_mask & (1 << d):
                    continue
                if pos < 2:
                    _build(pos + 1, used_mask | (1 << d), a_val * 10 + d, b_val)
                else:
                    _build(pos + 1, used_mask | (1 << d), a_val, b_val * 10 + d)

        _build(0, 0, 0, 0)
        return results

    p1 = _backtrack_split_one_four()
    p2 = _backtrack_split_two_three()
    pandigital_products = p1 | p2
    return sum(pandigital_products), pandigital_products


# ---------------------------------------------------------------------------
# Approach 4: Optimized brute-force with bitmask (no string operations)
# ---------------------------------------------------------------------------

def solution_bitmask_optimized():
    """Approach 4: Brute force + bitmask pandigital check — zero strings."""
    pandigital_products = set()

    # Precompute digit masks for single-digit numbers 1-9 and 4-digit numbers
    def _is_pandigital_combo(a, b, p):
        mask_a = _to_digit_mask(a)
        if mask_a < 0 or mask_a == 0:
            return False
        mask_b = _to_digit_mask(b)
        if mask_b < 0 or (mask_a & mask_b):
            return False
        mask_p = _to_digit_mask(p)
        if mask_p < 0 or (mask_p & (mask_a | mask_b)):
            return False
        return (mask_a | mask_b | mask_p) == 0x1FF

    # Split (1, 4)
    for a in range(1, 10):
        for b in range(1023, 9877):
            p = a * b
            if p > 9999:
                continue
            if _is_pandigital_combo(a, b, p):
                pandigital_products.add(p)

    # Split (2, 3)
    for a in range(12, 99):
        max_b = min(987, 9999 // a)
        for b in range(123, max_b + 1):
            p = a * b
            if p > 9999:
                continue
            if _is_pandigital_combo(a, b, p):
                pandigital_products.add(p)

    return sum(pandigital_products), pandigital_products


# ---------------------------------------------------------------------------
# Main — run all approaches and verify they agree
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import time

    approaches = [
        ("Brute-force (string-based)", solution_brute_force),
        ("Permutation", solution_permutation),
        ("Backtracking (bitmask)", solution_backtracking),
        ("Bitmask optimized", solution_bitmask_optimized),
    ]

    results = []
    for name, func in approaches:
        t0 = time.perf_counter()
        total, products = func()
        elapsed = (time.perf_counter() - t0) * 1000
        results.append((name, total, products))
        print(f"{name}: sum={total}, count={len(products)}, {elapsed:.2f}ms")

    # Verify all approaches agree
    totals = set(r[1] for r in results)
    if len(totals) == 1:
        print(f"\nAll approaches agree: answer = {totals.pop()}")
    else:
        print(f"\nMISMATCH! Results: {set(r[1] for r in results)}")
