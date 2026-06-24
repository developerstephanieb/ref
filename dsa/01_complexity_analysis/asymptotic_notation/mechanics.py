"""asymptotic_notation — mechanics.

Empirical-vs-derived demonstrations for asymptotic notation. This is the empirical
half: it measures the growth ratios f(n)/g(n) the README reasons about and asserts
that the measured trend matches the derived asymptotic class.

    python mechanics.py                 # run every section
    python mechanics.py --section ladder

Each function mirrors one README section, prints a labeled claim with the
measured ratios so the output is self-evidencing, and backs the claim with an
`assert_trend` over those ratios.

Assumes CPython >= 3.11.
"""

from __future__ import annotations

import argparse
import math
from collections.abc import Callable

Fn = Callable[[float], float]

# ---------------------------------------------------------------------------
# Helpers (reused across sections)
# ---------------------------------------------------------------------------


def log_factorial(n: int) -> float:
    """Return ln(n!) via `math.lgamma`, avoiding overflow for large n."""
    return math.lgamma(n + 1)


def growth_ratio(f: Fn, g: Fn, ns: list[float], label: str) -> list[float]:
    """Print and return f(n)/g(n) across *ns* so its trend is visible.

    The ratio is the empirical handle on a dominance claim: f ≪ g shows up as
    f/g → 0, f ≫ g as f/g → ∞, and f = Θ(g) as f/g → a positive constant.
    """
    ratios = [f(n) / g(n) for n in ns]
    print(f"  {label}")
    for n, r in zip(ns, ratios):
        print(f"    n={n:<12g} ratio={r:.6g}")
    return ratios


def crossover(f: Fn, g: Fn, lo: int, hi: int) -> int | None:
    """Smallest integer n in [lo, hi] with f(n) <= g(n), else None.

    Used for the 100n vs n² demo: it locates the n₀ past which the
    asymptotically larger function actually overtakes the smaller one.
    """
    for n in range(lo, hi + 1):
        if f(n) <= g(n):
            return n
    return None


def assert_trend(
    values: list[float],
    kind: str,
    *,
    target: float | None = None,
    rtol: float = 0.05,
    label: str = "",
) -> None:
    """Assert a ratio sequence follows *kind*, else raise AssertionError.

    kind:
      "to_zero"   strictly decreasing and arriving near 0 (f ≪ g)
      "to_inf"    strictly increasing without bound        (f ≫ g)
      "flat"      constant within *rtol*                   (f = Θ(g), c known)
      "to_value"  monotone and converging to *target*      (f = Θ(g) via limit)
    """
    pairs = list(zip(values, values[1:]))
    if kind == "to_zero":
        assert all(b < a for a, b in pairs), f"{label}: not strictly decreasing"
        assert values[-1] < 1e-2, f"{label}: tail {values[-1]:.3g} not near 0"
    elif kind == "to_inf":
        assert all(b > a for a, b in pairs), f"{label}: not strictly increasing"
        assert values[-1] > values[0], f"{label}: did not grow"
    elif kind == "flat":
        lo, hi = min(values), max(values)
        assert hi - lo <= rtol * abs(lo), f"{label}: spread {hi - lo:.3g} not flat"
    elif kind == "to_value":
        assert target is not None, f"{label}: to_value needs a target"
        mono = all(b < a for a, b in pairs) or all(b > a for a, b in pairs)
        assert mono, f"{label}: not monotone toward {target}"
        gap = abs(values[-1] - target)
        assert gap <= rtol * abs(target), f"{label}: tail off target by {gap:.3g}"
    else:  # pragma: no cover - guard against a typo in a caller
        raise ValueError(f"unknown trend kind: {kind!r}")


# ---------------------------------------------------------------------------
# Sections (one function per README section)
# ---------------------------------------------------------------------------


def s1_why() -> None:
    """Asymptotics compare growth, not machine time; constants are hidden."""
    print("s1 why-asymptotics: growth class, not wall-clock")

    # Two implementations of the same Θ(n) work with a 1000x constant gap rank
    # the SAME asymptotically — the constant is exactly what we discard.
    def slow(n):
        return 1000.0 * n

    def fast(n):
        return 1.0 * n

    ratios = growth_ratio(slow, fast, [10, 1e3, 1e6, 1e9], "1000n / n (constant gap)")
    assert_trend(ratios, "flat", label="constant factor is hidden")
    print("    -> both are Θ(n); the 1000x constant does not change the class\n")


def s2_big_o() -> None:
    """O is an upper bound; n₀ is why a bigger-O function can be faster small."""
    print("s2 big-o: the n₀ crossover (100n vs n²)")

    def f(n):  # O(n)
        return 100.0 * n

    def g(n):  # O(n²)
        return float(n) * n

    n0 = crossover(f, g, 1, 1000)
    print(f"    100n <= n² first at n={n0}")
    print(f"    n=50:  100n={f(50):g}  n²={g(50):g}  -> n² is SMALLER (faster)")
    print(f"    n=200: 100n={f(200):g}  n²={g(200):g}  -> n² is LARGER (slower)")
    assert n0 == 100, "crossover of 100n and n² must be exactly n=100"
    # Below n₀ the asymptotically larger n² is the faster choice; "O(n²) beats
    # O(n)" is only a statement about large n.
    assert g(50) < f(50) and g(200) > f(200)
    print("    -> O describes large-n growth; below n₀ the ranking can invert\n")


def s3_big_omega() -> None:
    """Ω is a lower bound: f stays at or above c·g for large n."""
    print("s3 big-omega: f bounded below by c·g")

    # f(n) = n²/2 - 3n is Ω(n²): for n ≥ 12, f(n) >= (1/4)·n²
    # (since (1/4)n² ≥ 3n ⇔ n ≥ 12). The sample starts at that n₀.
    def f(n):
        return 0.5 * n * n - 3.0 * n

    def g(n):
        return float(n) * n

    ratios = growth_ratio(f, g, [12, 100, 1e3, 1e4], "f / n²  ->  c≥1/4")
    # The ratio equals 1/4 at n=12 and rises to 1/2; below n=12 it dips under
    # 1/4 (and f(6)=0), which is exactly why n₀=12, not 6.
    assert all(r >= 0.25 for r in ratios), "f must sit above (1/4)·n² for n ≥ 12"
    assert_trend(ratios, "to_value", target=0.5, label="f = Ω(n²) (and Θ(n²))")
    print("    -> ∃ c=1/4, n₀=12 with f(n) ≥ c·n²  =>  f = Ω(n²)\n")


def s4_big_theta() -> None:
    """Θ sandwiches f between two constant multiples of g (both bounds proven)."""
    print("s4 big-theta: lower-order terms wash out -> Θ(n²)")

    def f(n):
        return 3.0 * n * n + 50.0 * n + 200.0

    def g(n):
        return float(n) * n

    ratios = growth_ratio(f, g, [10, 100, 1e3, 1e4, 1e5, 1e6], "(3n²+50n+200)/n²")
    # Sandwich: for n ≥ 10 the ratio sits in [3, 11]; it converges down to 3.
    assert all(3.0 <= r <= 11.0 for r in ratios), "ratio must stay in [c1,c2]"
    assert_trend(ratios, "to_value", target=3.0, label="f = Θ(n²)")
    print("    -> c1=3, c2=11, n₀=10 bound both sides  =>  Θ, not just O\n")


def s5_little_o_omega() -> None:
    """Strict bounds: o means the ratio goes to 0 (never tight)."""
    print("s5 little-o / little-omega: strict, via the limit")

    # n = o(n²): n/n² = 1/n -> 0, so the bound is never tight (unlike O).
    def f(n):
        return float(n)

    def g(n):
        return float(n) * n

    little_o = growth_ratio(f, g, [10, 100, 1e3, 1e4], "n / n²  (n = o(n²))")
    assert_trend(little_o, "to_zero", label="n = o(n²): ratio -> 0")
    # n² = ω(n): the reciprocal -> ∞.
    little_w = growth_ratio(g, f, [10, 100, 1e3, 1e4], "n² / n  (n² = ω(n))")
    assert_trend(little_w, "to_inf", label="n² = ω(n): ratio -> ∞")
    print("    -> o/ω are the strict (<,>) cousins of O/Ω; never tight\n")


def s6_simplification() -> None:
    """Drop constants and lower-order terms — within one variable only."""
    print("s6 simplification: the three rules, and their limits")

    # Rule: log base is a constant factor (change-of-base). log2 / ln is flat.
    base = growth_ratio(
        lambda n: math.log2(n),
        lambda n: math.log(n),
        [16, 1e3, 1e6, 1e12, 1e18],
        "log2(n) / ln(n)  ->  1/ln2",
    )
    assert_trend(base, "flat", label="log base is a constant factor")
    assert math.isclose(base[0], 1.0 / math.log(2), rel_tol=1e-12)

    # Rule: lower-order term drops WITHIN one variable. (n² + n)/n² -> 1.
    same_var = growth_ratio(
        lambda n: n * n + n,
        lambda n: float(n) * n,
        [10, 100, 1e3, 1e6],
        "(n² + n) / n²  ->  1  (drop +n)",
    )
    assert_trend(same_var, "to_value", target=1.0, label="n²+n = Θ(n²)")

    # Counter-rule: independent variables do NOT collapse. Hold n=1, grow m:
    # (n+m)/n = 1+m -> ∞, so n+m is NOT O(n).
    indep = growth_ratio(
        lambda m: 1.0 + m,
        lambda m: 1.0,
        [1, 10, 100, 1e3],
        "(n+m)/n with n=1, m growing  ->  ∞  (n+m ≠ O(n))",
    )
    assert_trend(indep, "to_inf", label="O(n+m) does not reduce to O(n)")
    print("    -> drop constants & lower-order terms; keep independent vars\n")


def s7_composition() -> None:
    """Sequence -> add then keep max; nest -> multiply; branch -> max."""
    print("s7 composition: combine block costs")

    def f(n):  # an O(n) block
        return float(n)

    def g(n):  # an O(n²) block
        return float(n) * n

    # Sequential: total = f + g; the sum is Θ(max(f,g)) = Θ(n²).
    seq = growth_ratio(
        lambda n: f(n) + g(n),
        g,
        [10, 100, 1e3, 1e4],
        "(n + n²) / n²  ->  1   (sequence = max term)",
    )
    assert_trend(seq, "to_value", target=1.0, label="seq f;g = Θ(max) = Θ(n²)")

    # Nested: total = f · g exactly = n·n² = n³ (a product, not a max).
    for n in (2, 5, 10, 50):
        assert f(n) * g(n) == float(n) ** 3, "nested loops multiply"
    print("    nested f×g = n·n² = n³  (product, verified exact)")

    # Branch: worst case of if/else is max(then, else), not their sum.
    for n in (1, 2, 10, 100):
        assert max(f(n), g(n)) == g(n), "branch worst case is the max branch"
    print("    branch max(n, n²) = n²  (worst of the two arms)\n")


def s8_growth_ladder() -> None:
    """Every dominance claim in §B3, driven through growth_ratio + assert_trend."""
    print("s8 growth-classes: the ladder, each separation verified")

    # n log n is strictly between n and n².
    above = growth_ratio(
        lambda n: n * math.log2(n) / n,
        lambda n: 1.0,
        [10, 1e3, 1e6, 1e9],
        "(n log n)/n = log n  ->  ∞   (n log n ≫ n)",
    )
    assert_trend(above, "to_inf", label="n log n ≫ n")
    below = growth_ratio(
        lambda n: math.log2(n) / n,
        lambda n: 1.0,
        [10, 1e3, 1e6, 1e9],
        "(n log n)/n² = (log n)/n  ->  0   (n log n ≪ n²)",
    )
    assert_trend(below, "to_zero", label="n log n ≪ n²")

    # Polynomial beats polylog (observable exponents; see module docstring).
    polylog = growth_ratio(
        lambda n: math.log2(n) ** 3,
        lambda n: float(n),
        [100, 1e3, 1e4, 1e6],
        "(log n)³ / n  ->  0   (polynomial ≫ polylog)",
    )
    assert_trend(polylog, "to_zero", label="n ≫ (log n)³")

    # Exponential beats polynomial: n⁵ / 2ⁿ -> 0.
    exp_poly = growth_ratio(
        lambda n: float(n) ** 5,
        lambda n: 2.0**n,
        [10, 20, 40, 60],
        "n⁵ / 2ⁿ  ->  0   (exponential ≫ polynomial)",
    )
    assert_trend(exp_poly, "to_zero", label="2ⁿ ≫ n⁵")

    # Factorial beats every fixed-base exponential: 2ⁿ / n! -> 0 (via lgamma).
    fact_exp = growth_ratio(
        lambda n: math.exp(n * math.log(2) - log_factorial(int(n))),
        lambda n: 1.0,
        [10, 20, 40, 80],
        "2ⁿ / n!  ->  0   (factorial ≫ exponential)",
    )
    assert_trend(fact_exp, "to_zero", label="n! ≫ 2ⁿ")

    # Exponent base is decisive (this is the D11 / exponent-base claim).
    base_lt = growth_ratio(
        lambda n: 2.0**n,
        lambda n: 3.0**n,
        [5, 10, 20, 40],
        "2ⁿ / 3ⁿ = (2/3)ⁿ  ->  0   (2ⁿ ≠ Θ(3ⁿ))",
    )
    assert_trend(base_lt, "to_zero", label="2ⁿ ≪ 3ⁿ")
    base_sq = growth_ratio(
        lambda n: 4.0**n,
        lambda n: 2.0**n,
        [2, 5, 10, 20],
        "4ⁿ / 2ⁿ = 2ⁿ  ->  ∞   (4ⁿ = 2^{2n} ≠ O(2ⁿ))",
    )
    assert_trend(base_sq, "to_inf", label="4ⁿ ≫ 2ⁿ")
    base_const = growth_ratio(
        lambda n: 2.0 ** (n + 1),
        lambda n: 2.0**n,
        [2, 5, 10, 20],
        "2^{n+1} / 2ⁿ = 2   (2^{n+1} = O(2ⁿ): +1 is a constant in the exponent)",
    )
    assert_trend(base_const, "flat", label="2^{n+1} = Θ(2ⁿ)")
    print("    -> 1 ≪ log n ≪ n ≪ n log n ≪ n² ≪ 2ⁿ ≪ 3ⁿ ≪ n!\n")


def s9_case_vs_bound() -> None:
    """Case (which input) and bound (which side) are orthogonal axes."""
    print("s9 case-vs-bound: orthogonal axes (insertion sort)")

    def insertion_sort_comparisons(data: list[int]) -> int:
        """Count comparisons — the empirical cost handle for insertion sort."""
        count = 0
        a = data[:]
        for i in range(1, len(a)):
            j = i
            while j > 0:
                count += 1  # the comparison a[j-1] > a[j]
                if a[j - 1] <= a[j]:
                    break
                a[j - 1], a[j] = a[j], a[j - 1]
                j -= 1
        return count

    n = 50
    best = insertion_sort_comparisons(list(range(n)))  # sorted: best case
    worst = insertion_sort_comparisons(list(range(n, 0, -1)))  # reversed: worst
    print(f"    n={n}: best (sorted) = {best} comparisons  ~ Θ(n) = {n - 1}")
    print(f"    n={n}: worst (reversed) = {worst} comparisons  ~ Θ(n²)/2")
    # Best case is linear (n-1 comparisons); worst is the triangular n(n-1)/2.
    assert best == n - 1, "sorted input: one comparison per element"
    assert worst == n * (n - 1) // 2, "reversed input: full triangular count"
    # Both cases admit BOTH a Big-O and a Big-Ω; bound and case are independent.
    print("    -> 'case' picks the input; 'bound' (O/Θ/Ω) wraps any chosen case\n")


SECTIONS = {
    "why": s1_why,
    "big_o": s2_big_o,
    "big_omega": s3_big_omega,
    "big_theta": s4_big_theta,
    "little": s5_little_o_omega,
    "simplification": s6_simplification,
    "composition": s7_composition,
    "ladder": s8_growth_ladder,
    "case_vs_bound": s9_case_vs_bound,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--section",
        choices=sorted(SECTIONS),
        help="run a single section instead of all of them",
    )
    args = parser.parse_args()

    to_run = [SECTIONS[args.section]] if args.section else list(SECTIONS.values())
    for func in to_run:
        func()
    print("asymptotic_notation: all trends hold")


if __name__ == "__main__":
    main()
