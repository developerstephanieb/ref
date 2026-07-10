Q: Why does `0.1 + 0.2 == 0.3` evaluate to False?
A: Floats are IEEE 754 binary64. 0.1, 0.2, and 0.3 have denominators that aren't powers of 2, so each is stored as the nearest double. The errors in stored 0.1 and 0.2 don't cancel to stored 0.3 — the sum is 0.30000000000000004.
TAGS: builtin_types float representation gotcha
---
Q: How many sign, exponent, and fraction bits does an IEEE 754 binary64 float have?
A: 1 sign bit, 11 exponent bits, 52 fraction bits — 64 total. The implicit leading 1 gives 53 bits of significand precision.
TAGS: builtin_types float representation concept
---
Q: What's the difference between the significand and the fraction of a float?
A: The significand is the full `1.f…` value — 53 bits including the implicit leading 1. The fraction is only the 52 stored bits after that leading 1. ("Mantissa" is an informal synonym for the fraction.)
TAGS: builtin_types float representation concept
---
Q: Which real numbers can a float represent exactly?
A: Only fractions whose denominator is a power of 2, that also fit within 53 bits of precision. Values like 0.1 or 1/3 have other prime factors in the denominator and so have no finite binary expansion.
TAGS: builtin_types float representation concept
---
Q: Why does `repr(0.1)` print "0.1" if the stored value isn't exactly 0.1?
A: `repr` prints the shortest decimal string that round-trips to the same double, so `float(repr(x)) == x`. "0.1" is the shortest string inside the rounding interval of the stored value, which is really 0.1000000000000000055511151231257827021181583404541015625.
TAGS: builtin_types float representation concept
---
Q: What is a ULP (unit in the last place)?
A: The spacing between a double and the next representable double at a given magnitude. It's constant between consecutive powers of two and doubles at each power-of-two boundary.
TAGS: builtin_types float representation concept
---
Q: `repr(x)` vs `Decimal(x)` — what does each give you for a float?
A: `repr(x)` gives the shortest decimal string that round-trips back to the same double — a label for it, e.g. `repr(0.1)` is "0.1". `Decimal(x)` gives the exact stored value, e.g. `Decimal(0.1)` is 0.1000000000000000055511151231257827021181583404541015625. Reach for repr to display or serialize; reach for `Decimal(x)` to inspect what's truly stored.
TAGS: builtin_types float representation concept
---
Q: How do you compare two floats for "equality"?
A: Use `math.isclose(a, b)` (relative tolerance, default rel_tol=1e-9). Never use `==` on computed floats.
TAGS: builtin_types float comparison concept
---
Q: What inequality does `math.isclose(a, b)` actually test?
A: `abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)`. Using max(|a|,|b|) makes it symmetric, so argument order never matters.
TAGS: builtin_types float comparison concept
---
Q: What are the default rel_tol and abs_tol of `math.isclose`, and what does each do?
A: rel_tol=1e-9 scales with the inputs (relative). abs_tol=0.0 is a fixed floor (absolute), needed when either argument may be 0.0.
TAGS: builtin_types float comparison concept
---
Q: Why does `math.isclose(0.0, 1e-10)` return False, and how do you fix it?
A: The relative buffer is rel_tol * max(|a|,|b|) = 1e-9 * 1e-10 = 1e-19, which is far less than the 1e-10 difference. Pass an absolute tolerance: `math.isclose(0.0, 1e-10, abs_tol=1e-9)`.
TAGS: builtin_types float comparison gotcha
---
Q: How does `numpy.isclose` differ from `math.isclose`?
A: numpy is asymmetric — `abs(a-b) <= atol + rtol*abs(b)` (the second arg is the reference) — with looser defaults rtol=1e-05, atol=1e-08. math.isclose is symmetric with rel_tol=1e-9, abs_tol=0.0.
TAGS: builtin_types float comparison concept
---
Q: How do you get exact decimal arithmetic, and what's the constructor trap?
A: Use `Decimal` from the decimal module, built from a STRING. `Decimal("0.1")` is exact; `Decimal(0.1)` inherits the binary float's error, so `Decimal(0.1) + Decimal(0.2) != Decimal("0.3")`.
TAGS: builtin_types float exact_alternatives gotcha
---
Q: When should you use `Decimal` vs `Fraction`?
A: `Decimal` is exact in base 10 but fixed-precision (default 28 digits) — for money/base-10 reporting; it can't represent 1/3. `Fraction` is exact for every rational with unbounded precision — for exact ratios — but its denominators grow as operations chain.
TAGS: builtin_types float exact_alternatives concept
---
Q: Can `Decimal` represent 1/3 exactly?
A: No. `Decimal` is fixed-precision (default 28 significant digits), so `Decimal(1)/Decimal(3)` is 0.3333… (28 threes), not exact. Use `Fraction(1, 3)` for an exact third.
TAGS: builtin_types float exact_alternatives concept
---
Q: Besides `Decimal`, what's a common way to represent money exactly?
A: Store amounts as a whole number of cents (the smallest unit) in an `int` and do all arithmetic in `int` — integers are always exact, with no precision limit. Divide by 100 only for display. e.g. `0.10 + 0.20 != 0.30`, but `10 + 20 == 30` cents.
TAGS: builtin_types float exact_alternatives concept
---
Q: `Fraction(0.1)` vs `Fraction("1/10")` — why do they differ?
A: `Fraction(0.1)` is built from the float, so it captures the double's exact stored value — 3602879701896397/36028797018963968 — carrying the binary error. `Fraction("1/10")` (or `Fraction(1, 10)`) parses the exact rational 1/10. Same constructor trap as `Decimal`: build from a string or integer pair, never from a float.
TAGS: builtin_types float exact_alternatives gotcha
---
Q: What rounding mode does Python's built-in `round()` use?
A: Round-half-to-even (banker's rounding) on genuine ties: `round(0.5)==0`, `round(1.5)==2`, `round(2.5)==2`, `round(3.5)==4`. It avoids the upward bias of always rounding ties up.
TAGS: builtin_types float rounding gotcha
---
Q: Why is `round(2.675, 2)` equal to 2.67, not 2.68?
A: It's a representation effect, not banker's rounding. 2.675 is stored as 2.67499999999999982…, strictly below the midpoint, so `round` rounds down — the tie rule never fires. Round a `Decimal("2.675")` for true base-10 rounding.
TAGS: builtin_types float rounding gotcha
---
Q: round-half-to-even vs round-half-up — what's the difference, and how do you get half-up?
A: Round-half-to-even (Python's `round()` and the IEEE 754 default) sends a tie to the nearest even digit, avoiding the upward bias of always rounding ties up: `round(0.5)` is 0, `round(2.5)` is 2. Round-half-up always pushes a tie away from zero. To get it, round a Decimal: `Decimal("2.5").quantize(Decimal("1"), rounding=ROUND_HALF_UP)`.
TAGS: builtin_types float rounding concept
---
Q: What is `float('nan') == float('nan')`?
A: False. nan is never equal to anything, including itself (so `nan != nan` is True). Detect a nan with `math.isnan`, never `==`.
TAGS: builtin_types float special_values gotcha
---
Q: Why can `nan in [nan]` be True while `float('nan') in [float('nan')]` is False?
A: CPython containers test identity (is it the same object?) before `==`. `nan in [nan]` is the same object, so identity matches. Two separate `float('nan')` objects fail identity and `==`, so the second is False.
TAGS: builtin_types float special_values gotcha
---
Q: How do nan and inf differ in ordering comparisons?
A: inf is ordered — greater than any finite value. nan is unordered — every `<`, `>`, `<=`, `>=` against it is False, which silently breaks sorting.
TAGS: builtin_types float special_values concept
---
Q: Why does a stray `nan` silently corrupt `sorted()` and `max()`?
A: Every comparison involving nan returns False, so sort/selection can't place it consistently — no error is raised and the result depends on the nan's position. e.g. `max([nan, 1, 2, 3])` is nan but `max([1, 2, 3, nan])` is 3.0. Screen out nan first with `math.isnan`.
TAGS: builtin_types float special_values gotcha
---
Q: What does `float('inf') - float('inf')` evaluate to?
A: nan — an indeterminate form. Other indeterminate forms are `inf / inf` and `0.0 * inf`. Well-defined cases stay finite/inf: `inf + 1` is inf, `1 / inf` is 0.0.
TAGS: builtin_types float special_values gotcha
---
Q: Is overflow uniform in Python — does "too big" always give inf?
A: No. A too-large literal (1e400) and basic arithmetic (1e308 * 10) silently give inf, but `**` and many math functions raise OverflowError (`2.0 ** 2000`, `math.exp(1000)`).
TAGS: builtin_types float special_values gotcha
---
Q: Does `0 / 0` produce nan in Python?
A: No — it raises ZeroDivisionError. nan is reached only through inf arithmetic, e.g. `inf - inf`, `inf / inf`, `0.0 * inf`.
TAGS: builtin_types float special_values gotcha
---
Q: How are inf and nan encoded in an IEEE 754 binary64 float?
A: Both have an all-ones exponent field. inf has an all-zero fraction (sign picks ±inf); nan has a nonzero fraction. They're ordinary floats with a reserved bit pattern, so `type(float('nan'))` is float.
TAGS: builtin_types float special_values concept
---
Q: Is `==` always wrong for floats?
A: No — it's unreliable for COMPUTED floats. Exactly representable results are fine: `0.5 + 0.5 == 1.0` is True, while `0.1 + 0.2 == 0.3` is False. Treat `==` on arithmetic results as unreliable, not always-false.
TAGS: builtin_types float comparison concept
---
Q: Up to what magnitude can a float represent every integer exactly?
A: 2**53 (9007199254740992). Beyond it consecutive integers collapse: `float(2**53) == float(2**53 + 1)` is True. Keep large IDs as int; don't round-trip them through float.
TAGS: builtin_types float precision gotcha
---
Q: Why does `{1: "a", 1.0: "b"}` produce a dict with a single key?
A: `1 == 1.0` and `hash(1) == hash(1.0)`, so they are the same dict key; the later value wins, leaving `{1: "b"}`. The eq/hash invariant (equal objects must hash equal) is a data-model rule — see the data-model topic for its full contract.
TAGS: builtin_types float comparison gotcha
---
Q: A running float total in a `+=` loop drifts from the true sum — what's the fix?
A: Use `math.fsum(values)`, which tracks the exact partial sums and rounds once at
the end, returning the correctly rounded (exact) total.
TAGS: builtin_types float representation gotcha
---
Q: Why is `-7.5 // 2` equal to -4.0 and not -3.0?
A: `//` floors toward negative infinity (not truncates toward zero): -3.75 floors to -4.0. The remainder takes the sign of the divisor, so `-7.5 % 2` is 0.5, keeping `a == b*(a//b) + (a%b)`.
TAGS: builtin_types float division gotcha
