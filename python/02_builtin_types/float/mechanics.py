"""float — mechanics.

Runnable, assert-backed demonstrations of Python float behavior, and the
verification source of truth for README.md: every value, output, and bit
pattern quoted in the doc is produced here by running code.

    python mechanics.py                            # run every section
    python mechanics.py --section special_values   # run one section (see --help)

Each function mirrors one README section, prints a labeled claim with its
result so the output is self-evidencing, and backs the claim with `assert`s.
A failing assert means CPython's behavior drifted from what the doc states.

Assumes CPython >= 3.11; the compensated-`sum()` demonstration additionally
needs CPython >= 3.12 (guarded at runtime). Stdlib only.
"""

from __future__ import annotations

import argparse
import math
import struct
import sys
from decimal import ROUND_HALF_UP, Decimal, getcontext, localcontext
from fractions import Fraction

# ---------------------------------------------------------------------------
# Helpers (reused across sections)
# ---------------------------------------------------------------------------


def bits(x: float) -> str:
    """Return the IEEE 754 binary64 bit layout of *x* as 'sign exp fraction'."""
    (packed,) = struct.unpack(">Q", struct.pack(">d", x))
    raw = format(packed, "064b")
    return f"{raw[0]} {raw[1:12]} {raw[12:]}"


def exact(x: float) -> Decimal:
    """Return the exact stored value of the double *x* (no rounding)."""
    return Decimal(x)


def ulp(x: float) -> float:
    """Return the unit in the last place at *x*: the spacing to its neighbor."""
    return math.ulp(x)


def rounding_interval(x: float) -> tuple[Decimal, Decimal]:
    """Return the exact (lower, upper) reals that round to the double *x*.

    The boundaries are the midpoints to *x*'s two neighboring doubles.
    """
    below = math.nextafter(x, -math.inf)
    above = math.nextafter(x, math.inf)
    with localcontext() as ctx:
        ctx.prec = 80  # enough to show the full ~55-digit expansion exactly
        lower = (Decimal(below) + Decimal(x)) / 2
        upper = (Decimal(x) + Decimal(above)) / 2
    return lower, upper


def claim(label: str, value: object) -> None:
    """Print a labeled claim and its computed result."""
    print(f"  {label}: {value!r}")


# ---------------------------------------------------------------------------
# Sections (one per README section)
# ---------------------------------------------------------------------------


def why_inexact() -> None:
    """Why floats are imprecise: rounding to the nearest representable double."""
    print("Why floats are imprecise")
    claim("0.1 + 0.2 == 0.3", 0.1 + 0.2 == 0.3)
    claim("0.1 + 0.2", 0.1 + 0.2)
    assert 0.1 + 0.2 != 0.3
    assert 0.1 + 0.2 == 0.30000000000000004

    # 0.5 + 0.5 == 1.0 shows == is unreliable, not always wrong.
    claim("0.5 + 0.5 == 1.0", 0.5 + 0.5 == 1.0)
    assert 0.5 + 0.5 == 1.0

    # The exact stored values (Decimal(float) is exact) explain the failure.
    claim("exact(0.1)", str(exact(0.1)))
    claim("exact(0.2)", str(exact(0.2)))
    claim("exact(0.1 + 0.2)", str(exact(0.1 + 0.2)))
    claim("exact(0.3)", str(exact(0.3)))
    assert (
        str(exact(0.1)) == "0.1000000000000000055511151231257827021181583404541015625"
    )
    assert str(exact(0.2)) == "0.200000000000000011102230246251565404236316680908203125"
    assert str(exact(0.3)) == "0.299999999999999988897769753748434595763683319091796875"
    # The rounded sum lands on a different double than stored 0.3 (the README's
    # side-by-side); its exact value is what `0.1 + 0.2` actually holds.
    assert exact(0.1 + 0.2) == Decimal(
        "0.3000000000000000444089209850062616169452667236328125"
    )
    # stored 0.1 is slightly LARGER than 1/10
    assert exact(0.1) > Decimal("0.1")

    # Bit layout of 0.6875 == 0.1011_2 (the README worked example).
    claim("bits(0.6875)", bits(0.6875))
    assert bits(0.6875) == (
        "0 01111111110 0110000000000000000000000000000000000000000000000000"
    )

    # repr prints the shortest round-tripping string; float(repr(x)) == x.
    claim("repr(0.1)", repr(0.1))
    claim("float(repr(0.1)) == 0.1", float(repr(0.1)) == 0.1)
    assert repr(0.1) == "0.1"
    assert float(repr(0.1)) == 0.1

    # The rounding interval that all round-trip to the double nearest 0.1.
    lower, upper = rounding_interval(0.1)
    claim("rounding_interval(0.1) lower", str(lower))
    claim("rounding_interval(0.1) upper", str(upper))
    assert str(lower) == "0.099999999999999998612221219218554324470460414886474609375"
    assert str(upper) == "0.100000000000000012490009027033011079765856266021728515625"

    # A ULP is the spacing to the next double (math.ulp). It is constant between
    # consecutive powers of two and doubles at each power-of-two boundary.
    claim("ulp(1.0)", ulp(1.0))
    claim("ulp(2.0)", ulp(2.0))
    assert ulp(1.0) == math.ulp(1.0)
    assert ulp(2.0) == 2 * ulp(1.0)  # doubles crossing the 2**1 boundary


def comparison() -> None:
    """Comparing floats: math.isclose and the near-zero collapse."""
    print("Comparing floats")
    claim("math.isclose(0.1 + 0.2, 0.3)", math.isclose(0.1 + 0.2, 0.3))
    assert math.isclose(0.1 + 0.2, 0.3)

    # Default abs_tol is 0.0 and the relative buffer collapses against zero.
    claim("math.isclose(0.0, 1e-10)", math.isclose(0.0, 1e-10))
    claim(
        "math.isclose(0.0, 1e-10, abs_tol=1e-9)", math.isclose(0.0, 1e-10, abs_tol=1e-9)
    )
    assert not math.isclose(0.0, 1e-10)
    assert math.isclose(0.0, 1e-10, abs_tol=1e-9)

    # The test is symmetric: max(|a|, |b|) means argument order never matters.
    claim(
        "isclose(a, b) == isclose(b, a)",
        math.isclose(1.0, 1.0 + 1e-12) == math.isclose(1.0 + 1e-12, 1.0),
    )
    assert math.isclose(1.0, 1.0 + 1e-12) == math.isclose(1.0 + 1e-12, 1.0)


def exact_alternatives() -> None:
    """When you need exactness: Decimal vs Fraction."""
    print("When you need exactness")
    # Decimal is exact for decimals -- but ONLY when built from a string.
    claim(
        'Decimal("0.1") + Decimal("0.2") == Decimal("0.3")',
        Decimal("0.1") + Decimal("0.2") == Decimal("0.3"),
    )
    claim(
        'Decimal(0.1) + Decimal(0.2) == Decimal("0.3")',
        Decimal(0.1) + Decimal(0.2) == Decimal("0.3"),
    )
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
    assert Decimal(0.1) + Decimal(0.2) != Decimal("0.3")

    # Decimal is fixed-precision: it cannot hold 1/3.
    claim("getcontext().prec", getcontext().prec)
    claim("Decimal(1) / Decimal(3)", str(Decimal(1) / Decimal(3)))
    assert getcontext().prec == 28
    assert str(Decimal(1) / Decimal(3)) == "0.3333333333333333333333333333"

    # Fraction is exact for every rational, but denominators grow.
    claim(
        "Fraction(1,10) + Fraction(2,10) == Fraction(3,10)",
        Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10),
    )
    chained = sum((Fraction(1, n) for n in range(1, 11)), Fraction(0))
    claim("sum(1/1 .. 1/10) as Fraction", chained)
    assert Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10)
    assert chained == Fraction(7381, 2520)

    # Constructor trap (mirrors Decimal): Fraction(float) imports the binary error,
    # Fraction(str) is exact. Fraction(0.1) is the exact stored value of the double.
    claim("Fraction(0.1)", Fraction(0.1))
    claim('Fraction("1/10")', Fraction("1/10"))
    assert Fraction(0.1) == Fraction(3602879701896397, 36028797018963968)
    assert Fraction("1/10") == Fraction(1, 10)
    assert Fraction(0.1) != Fraction("1/10")

    # Integer cents: holding money as whole cents in an int stays exact where the
    # float version does not.
    claim("0.10 + 0.20 == 0.30  (float dollars)", 0.10 + 0.20 == 0.30)
    claim("10 + 20 == 30  (int cents)", 10 + 20 == 30)
    assert (0.10 + 0.20 == 0.30) is False
    assert 10 + 20 == 30


def rounding() -> None:
    """Rounding with round(): round-half-to-even, and the 2.675 trap."""
    print("Rounding with round()")
    # round() is round-half-to-even (banker's rounding) on genuine ties.
    for value, expected in [(0.5, 0), (1.5, 2), (2.5, 2), (3.5, 4)]:
        claim(f"round({value})", round(value))
        assert round(value) == expected

    # 2.675 is NOT a tie: it is stored just below the midpoint, so it rounds down.
    claim("exact(2.675)", str(exact(2.675)))
    claim("round(2.675, 2)", round(2.675, 2))
    assert str(exact(2.675)) == "2.67499999999999982236431605997495353221893310546875"
    assert round(2.675, 2) == 2.67

    # Decimal on the true value gives the human answer with explicit rounding.
    claim(
        'Decimal("2.675").quantize(.01, ROUND_HALF_UP)',
        str(Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
    )
    assert Decimal("2.675").quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    ) == Decimal("2.68")


def special_values() -> None:
    """Special values: nan (unordered, self-unequal) and inf (ordered)."""
    print("Special values")
    nan = float("nan")
    inf = float("inf")

    # nan is self-unequal and unordered.
    claim("nan != nan", nan != nan)
    claim("nan < 1.0", nan < 1.0)
    assert nan != nan
    assert not (nan == nan)
    assert not (nan < 1.0) and not (nan > 1.0)
    assert not (nan <= nan) and not (nan >= 0.0)
    assert math.isnan(nan)
    # nan/inf are ordinary float objects carrying a reserved bit pattern.
    claim("type(float('nan')) is float", type(float("nan")) is float)
    assert type(float("nan")) is float

    # Identity beats value: containers test `is` before `==`.
    claim("nan in [nan]  (same object)", nan in [nan])
    claim("float('nan') in [float('nan')]  (distinct)", float("nan") in [float("nan")])
    claim("len({float('nan'), float('nan')})", len({float("nan"), float("nan")}))
    assert nan in [nan]
    assert float("nan") not in [float("nan")]
    assert len({float("nan"), float("nan")}) == 2
    assert len({nan, nan}) == 1

    # A stray nan corrupts max()/min() depending on position (sorted() too).
    claim("max([nan, 1.0, 2.0, 3.0])", max([nan, 1.0, 2.0, 3.0]))
    claim("max([1.0, 2.0, 3.0, nan])", max([1.0, 2.0, 3.0, nan]))
    assert math.isnan(max([nan, 1.0, 2.0, 3.0]))
    assert max([1.0, 2.0, 3.0, nan]) == 3.0

    # inf IS ordered, and a too-large literal becomes inf silently.
    claim("inf > 1e308", inf > 1e308)
    claim("1e400 == inf", 1e400 == inf)
    claim("sys.float_info.max", sys.float_info.max)
    assert inf == math.inf
    assert inf > 1e308 and -inf < -1e308
    assert 1e400 == inf
    # The largest finite double; exceeding it (by arithmetic/literals) yields inf.
    assert sys.float_info.max == 1.7976931348623157e308

    # Most inf arithmetic is well-defined; indeterminate forms decay to nan.
    claim("inf + 1", inf + 1)
    claim("1 / inf", 1 / inf)
    claim("math.isnan(inf - inf)", math.isnan(inf - inf))
    assert inf + 1 == inf and inf * 2 == inf and 1 / inf == 0.0
    assert math.isnan(inf - inf)
    assert math.isnan(inf / inf)
    assert math.isnan(0.0 * inf)

    # 0/0 does NOT give nan -- it raises. The route to nan is via inf.
    try:
        _ = 0 / 0
    except ZeroDivisionError:
        claim("0 / 0 raises", "ZeroDivisionError")
    else:  # pragma: no cover - defensive
        raise AssertionError("0 / 0 did not raise")

    # Overflow is non-uniform: ** and many math funcs raise, arithmetic gives inf.
    for label, thunk in [
        ("2.0 ** 2000", lambda: 2.0**2000),
        ("math.exp(1000)", lambda: math.exp(1000)),
    ]:
        try:
            thunk()
        except OverflowError:
            claim(f"{label} raises", "OverflowError")
        else:  # pragma: no cover - defensive
            raise AssertionError(f"{label} did not raise OverflowError")
    claim("1e308 * 10", 1e308 * 10)
    claim("1e308 + 1e308", 1e308 + 1e308)
    assert 1e308 * 10 == inf
    assert 1e308 + 1e308 == inf

    # isclose treats specials by its normal rules.
    claim("isclose(inf, inf)", math.isclose(inf, inf))
    claim("isclose(inf, -inf)", math.isclose(inf, -inf))
    claim("isclose(nan, nan)", math.isclose(nan, nan))
    assert math.isclose(inf, inf)
    assert not math.isclose(inf, -inf)
    assert not math.isclose(nan, nan)

    # Encodings: inf has all-1 exponent + zero fraction; nan has nonzero fraction.
    claim("bits(inf)", bits(inf))
    claim("bits(nan)", bits(nan))
    assert bits(inf).split()[1] == "1" * 11
    assert set(bits(inf).split()[2]) == {"0"}
    assert bits(nan).split()[1] == "1" * 11
    assert set(bits(nan).split()[2]) != {"0"}


def precision_limits() -> None:
    """Integers as floats: the 2**53 collapse and shared int/float keys."""
    print("Integers as floats")
    claim("2**53", 2**53)
    claim("float(2**53) == float(2**53 + 1)", float(2**53) == float(2**53 + 1))
    assert 2**53 == 9007199254740992
    assert float(2**53) == float(2**53 + 1)
    assert 2.0**53 + 1 == 2.0**53

    # An int and an equal-valued float share a hash, so they collide as keys.
    # Built via dict([...]) so the literal {1: "a", 1.0: "b"} isn't flagged as a
    # repeated key -- the collision is exactly the behavior being demonstrated.
    d = dict([(1, "a"), (1.0, "b")])
    claim('{1: "a", 1.0: "b"}', d)
    claim("hash(1) == hash(1.0)", hash(1) == hash(1.0))
    claim("issubclass(int, float)", issubclass(int, float))
    assert d == {1: "b"}
    assert hash(1) == hash(1.0)
    assert issubclass(int, float) is False


def division_modulo() -> None:
    """Floor division: // floors toward -inf; % takes the sign of the divisor."""
    print("Floor division")
    claim("-7.5 // 2", -7.5 // 2)
    claim("-7.5 % 2", -7.5 % 2)
    claim("7.5 // 2", 7.5 // 2)
    assert -7.5 // 2 == -4.0
    assert -7.5 % 2 == 0.5
    assert 7.5 // 2 == 3.0
    # The division identity a == b*(a//b) + (a % b) holds exactly here.
    assert -7.5 == 2 * (-7.5 // 2) + (-7.5 % 2)


def gotchas() -> None:
    """Closing gotchas: accumulation error and fsum; nan-vs-sort recap."""
    print("Gotchas (cross-cutting)")
    # A manual += running total drifts; fsum is correctly rounded (exact).
    acc = 0.0
    for _ in range(10):
        acc += 0.1
    claim("manual += 0.1 x10", acc)
    claim("math.fsum([0.1] * 10)", math.fsum([0.1] * 10))
    assert acc == 0.9999999999999999
    assert acc != 1.0
    assert math.fsum([0.1] * 10) == 1.0

    # CPython 3.12+ also made the built-in sum() compensated for floats.
    if sys.version_info >= (3, 12):
        claim("sum([0.1] * 10)  (3.12+ compensated)", sum([0.1] * 10))
        assert sum([0.1] * 10) == 1.0


SECTIONS = {
    "why_inexact": why_inexact,
    "comparison": comparison,
    "exact_alternatives": exact_alternatives,
    "rounding": rounding,
    "special_values": special_values,
    "precision_limits": precision_limits,
    "division_modulo": division_modulo,
    "gotchas": gotchas,
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
    print("float: all assertions hold")


if __name__ == "__main__":
    main()
