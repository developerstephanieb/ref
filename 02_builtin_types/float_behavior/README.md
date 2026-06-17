# Float Behavior

Why Python floats misbehave, how to work around it, and the special-value
traps (`nan`, `inf`) that show up in interviews and production alike.

---

## Why floats are imprecise

A Python `float` is an IEEE 754 **binary64** (double): 1 sign bit, 11 exponent
bits, 52 fraction bits.

A float stores a number as a sign times a **significand** scaled by a power of two:

$$(-1)^{\text{sign}} \times \underbrace{1.f_1 f_2 \dots f_{52}}_{\text{significand}} \times 2^{\text{exponent}}$$

So a value is exactly representable only when it is a fraction whose denominator is a power of $2$ — and it fits within 53 bits of precision. Many short decimals — `0.1`,
`0.2`, `0.3` — have denominators that are not powers of $2$, so they have no finite binary
expansion, exactly like $\frac{1}{3}$ has no finite decimal expansion. Each is stored as
the nearest representable double.

```python
0.1 + 0.2 == 0.3      # False
0.1 + 0.2             # 0.30000000000000004
```

The errors are tiny but real: the doubles nearest `0.1` and `0.2` sum to a value
whose nearest double is not the double nearest `0.3`.

`repr()` hides the approximation by printing the shortest decimal string that
round-trips back to the identical double — which is why `repr(0.1) == "0.1"` even
though the exact stored value of `0.1` is

```
0.1000000000000000055511151231257827021181583404541015625
```

---

<details>
<summary><b>How any base represents fractions (radix &amp; negative powers)</b></summary>

Human arithmetic uses base 10 (decimal); computer hardware uses base 2 (binary).
The same positional rule governs both: digits to the right of the point are coefficients
of negative powers of the base.

In base 10, the digit positions after the point carry weights $10^{-1}, 10^{-2}, \dots$:

$$0.375_{10} = (3 \times 10^{-1}) + (7 \times 10^{-2}) + (5 \times 10^{-3}) = \tfrac{3}{10} + \tfrac{7}{100} + \tfrac{5}{1000}$$

In base 2, the positions carry weights $2^{-1}, 2^{-2}, \dots$:

$$0.011_{2} = (0 \times 2^{-1}) + (1 \times 2^{-2}) + (1 \times 2^{-3}) = \tfrac{1}{4} + \tfrac{1}{8} = 0.375_{10}$$

**Takeaway:** a binary fraction can only be built by adding pieces like
$\frac{1}{2}, \frac{1}{4}, \frac{1}{8}, \frac{1}{16}, \dots$.

</details>

<details>
<summary><b>Which fractions terminate (finite vs. infinite expansions)</b></summary>

A fraction (in **lowest terms** — numerator and denominator share no common factor)
has a finite expansion in a given base if and only if its denominator's prime factors
are all factors of that base.

* **Base 10** — prime factors of $10$ are $2$ and $5$. So $\frac{1}{3}$ never terminates
  ($0.3333\ldots$) because $3$ is not among them.
* **Base 2** — the only prime factor of $2$ is $2$. So a fraction terminates only if its
  denominator is a power of $2$.

When you write `0.1`, you mean $\frac{1}{10}$. Since $10 = 2 \times 5$ and $5$ is not a
power of $2$, one-tenth cannot be written finitely in binary — it repeats forever:

$$0.1_{10} = 0.0001100110011001100110011\ldots_2 \quad (\text{the block } 0011 \text{ repeats})$$

This is the root cause of every "floating-point surprise": the number is wrong before
any arithmetic happens, simply because it can't be written down exactly.

</details>

<details>
<summary><b>Binary scientific notation &amp; normalization (the hidden bit)</b></summary>

Computers store numbers in a binary version of scientific notation. In base 10 you might
write $-1.23 \times 10^{4}$, which has a sign (negative), a **significand** ($1.23$), and an exponent ($4$). Applied
to base 2:

$$(-1)^{\text{sign}} \times \underbrace{1.f_1 f_2 \dots}_{\text{significand}} \times 2^{\text{exponent}}$$

**Normalization** means shifting the binary point so exactly one `1` sits in front of it.
Consider $0.1011_2$:

* **Start:** $0.1011_2$
* **Normalized:** $1.011_2 \times 2^{-1}$  (point shifted right one place, compensated by $2^{-1}$)

Because a normalized binary number always begins with `1.`, that leading bit carries no
information — so the hardware drops and assumes it. This is the **implicit (hidden) bit**, and it is why 52 stored fraction bits yield 53 bits of precision.

</details>

<details>
<summary><b>Packing it into 64 bits (the IEEE 754 binary64 layout)</b></summary>

The binary64 format uses exactly 64 bits, partitioned as:

* **Sign (1 bit):** $0$ positive, $1$ negative.
* **Exponent (11 bits):** the scale (power of $2$), stored with a **bias** of $1023$ — the
  field holds (true exponent $+ 1023$). The bias lets a single unsigned field represent
  both positive and negative exponents without a separate sign.
* **Fraction (52 bits):** the bits after the implicit leading `1`, i.e. coefficients of
  $2^{-1}, 2^{-2}, \dots$ within the significand.

**Worked example — storing $0.1011_2$:**

Normalized form is $1.011_2 \times 2^{-1}$.

1. **Sign:** `0` (positive).
2. **Exponent:** true exponent is $-1$, so the stored field is $-1 + 1023 = 1022 =$
   `01111111110`.
3. **Fraction:** drop the implicit `1.`, store what follows the binary point — `011` — then
   pad to 52 bits: `0110000…0`.

The full 64-bit pattern is `0 01111111110 0110000000000000000000000000000000000000000000000000`.
You can dump these raw bytes for any float in Python with `struct.pack('>d', x)` (`'>d'`
is a big-endian double); unpacking them to an integer and reading off the bits is how
`mechanics.py` produces the breakdowns shown here.

> **Terminology note.** IEEE 754 calls the full $1.f_1 f_2 \dots$ value the
> significand (53 bits, including the implicit leading bit). The 52 stored bits are
> its fraction (or trailing significand). "Mantissa" is a common informal synonym
> for the fraction.

**Reserved exponent encodings.** Two of the $2^{11}=2048$ exponent values are special: an
all-zeros field marks **subnormal** numbers (no hidden `1`; used for values very close to
zero, and zero itself), and an all-ones field marks ±∞ and NaN (see § Special values).
That is why the usable true-exponent range is about $-1022$ to $+1023$ rather than the full
$\pm1023$.

</details>

<details>
<summary><b>Rounding to the nearest representable double (and what a ULP is)</b></summary>

With only 53 bits of precision, an infinitely repeating value like `0.1` must be cut off.
Two different stages do this rounding, both following the same IEEE 754 default rule:

* **Conversion** — turning the source literal `0.1` into a double.
* **Arithmetic** — computing `0.1 + 0.2`. This is done by the **FPU** (floating-point unit,
  the CPU's hardware for float math), which keeps a few extra low-order bits beyond the 52
  it will store and uses them to decide which way to round. Those scratch bits are the
  **guard**, **round**, and **sticky** bits: the guard and round bits are the first two bits
  past the kept 52, and the sticky bit is the OR of everything below them (it records
  "something nonzero remains"). Together they say whether the discarded tail is above,
  below, or exactly at half a ULP.

A **ULP** ("unit in the last place") is the spacing between a double and the next
representable double at a given magnitude — the value of the lowest stored bit. Python exposes the ULP at a given magnitude directly
as `math.ulp(x)`.

**The rule (round half to even):**

* discarded tail more than half a ULP → round up (increment the last kept bit),
* less than half → round down (truncate),
* exactly half → round so the last kept bit is even. This default is called
  **banker's rounding** (round-half-to-even); it avoids the upward bias of always rounding
  ties up (see § Rounding with `round()`).

So the value actually stored for `0.1` is not $\frac{1}{10}$ but:

```
0.1000000000000000055511151231257827021181583404541015625
```

And the famous failure compounds two such errors:

```
exact stored 0.1   = 0.1000000000000000055511151231257827021181583404541015625
exact stored 0.2   = 0.200000000000000011102230246251565404236316680908203125
their sum (rounded)= 0.3000000000000000444089209850062616169452667236328125  ->  0.30000000000000004
exact stored 0.3   = 0.299999999999999988897769753748434595763683319091796875
```

The sum lands on a different double than the one nearest `0.3`, so `0.1 + 0.2 == 0.3` is
`False`.

</details>

<details>
<summary><b><code>repr()</code> and the shortest round-trip</b></summary>

`repr()` prints the shortest decimal string that round-trips to the same double.

A **round-trip** is: float → string → float, landing back on the identical bit pattern.

Because doubles are discrete, each one "owns" a **rounding interval** — the interval of
real numbers that round to it. Any decimal string inside that interval parses back to the
same double. `repr()`'s algorithm:

1. Identify the exact double currently in memory.
2. Compute the lower and upper boundaries of its rounding interval (the midpoints to its
   two neighboring doubles).
3. Among all decimal strings inside that interval, pick the shortest.

For the double representing `0.1`, the interval boundaries are:

```
lower = 0.099999999999999998612221219218554324470460414886474609375
upper = 0.100000000000000012490009027033011079765856266021728515625
```

Inside this band live strings like `0.10000000000000001` and `0.09999999999999999` (17
digits each) — but also `0.1` (1 digit). Since `"0.1"` falls inside the interval and is the
shortest, `repr(0.1)` returns `"0.1"`. The short string is a label for the
double, not its exact value.

</details>

<details>
<summary><b>Accumulated rounding: summing many floats</b></summary>

Every `+` re-rounds its result to the nearest double, so a naive running total accumulates
those tiny errors. Adding `0.1` ten times in a loop drifts off the true value:

```python
total = 0.0
for _ in range(10):
    total += 0.1
total            # 0.9999999999999999  (not 1.0)
```

`math.fsum` avoids the drift by tracking the exact partial sums and rounding only once at
the end, so it returns the correctly rounded (exact) total:

```python
math.fsum([0.1] * 10)    # 1.0
```

A wrinkle on the built-in `sum()`: as of CPython 3.12 it uses compensated (Neumaier)
summation for floats, so `sum([0.1] * 10) == 1.0` too. But that is a CPython
implementation detail, and `sum()` is still not guaranteed correctly rounded for every
input — `math.fsum` is. Reach for `fsum` when an exact sum matters.

</details>

---

## Comparing floats

Don't use `==` on computed floats (results of arithmetic). `==` asks whether two values
are the exact same double; rounding makes that unreliable — `0.1 + 0.2 == 0.3` is
`False`. (It is unreliable, not always wrong: `0.5 + 0.5 == 1.0` is `True`, because both
operands and the result are exactly representable.) Use `math.isclose`, which asks instead
whether two values are within a tolerance. By default it checks a **relative** tolerance
(`rel_tol=1e-9`):

```python
math.isclose(0.1 + 0.2, 0.3)        # True
```

**Gotcha near zero.** When one argument is `0.0`, the relative test reduces to
$|x| \le \text{rel\_tol} \times |x|$, which is `False` for every nonzero `x`. Pass an
**absolute** tolerance (`abs_tol`) whenever a side may be zero:

```python
math.isclose(0.0, 1e-10)                # False  <- the zero-collapse trap
math.isclose(0.0, 1e-10, abs_tol=1e-9)  # True
```

<details>
<summary><b>How <code>math.isclose</code> decides — the tolerance formula</b></summary>

`math.isclose(a, b)` doesn't test equality; it tests a single inequality, returning `True`
if and only if the **absolute difference** $|a - b|$ is within the larger of the
relative and absolute tolerances:

$$|a - b| \le \max\!\left(\text{rel\_tol} \times \max(|a|, |b|),\ \text{abs\_tol}\right)$$

**Relative tolerance** (`rel_tol`, default $10^{-9}$ — one billionth) is a multiplier that
scales with the inputs: it permits a wider absolute difference for numbers in the millions
than for numbers near a thousandth. Scaling by $\max(|a|, |b|)$ makes the test
**symmetric** — `isclose(a, b)` equals `isclose(b, a)`, so argument order never matters.

**Why it collapses near zero.** With $a = 0$, $b = 10^{-10}$, and the defaults:

* absolute difference: $|0 - 10^{-10}| = 10^{-10}$
* relative buffer: $10^{-9} \times \max(0, 10^{-10}) = 10^{-19}$
* test: $10^{-10} \le \max(10^{-19}, 0) \implies 10^{-10} \le 10^{-19} \implies$ **False**

The buffer is `rel_tol ×` the nonzero value itself, so it's always a tiny fraction of the
value you're testing — far smaller than the absolute difference. Any nonzero float "fails"
against `0.0`.

**Absolute tolerance** (`abs_tol`, default `0.0`) is the fix: a fixed floor that doesn't
scale. With `abs_tol=1e-9`, the `max()` selects the larger of the collapsed $10^{-19}$ and
the fixed $10^{-9}$, letting the $10^{-10}$ difference pass.

</details>

<details>
<summary><b>For contrast: <code>numpy.isclose</code> is asymmetric with looser defaults</b></summary>

Note that `numpy.isclose` uses a different formula and different defaults. It is **asymmetric**
— the second argument `b` is the reference:

$$|a - b| \le \text{atol} + \text{rtol} \times |b|$$

So `numpy.isclose(a, b)` and `numpy.isclose(b, a)` can disagree, whereas `math.isclose` is
symmetric. Its defaults are also looser: `rtol=1e-05`, `atol=1e-08` (versus stdlib's
`rel_tol=1e-09`, `abs_tol=0.0`). Notably NumPy's nonzero default `atol` means its `isclose`
does not collapse against `0.0` the way the stdlib's does. Don't assume the two libraries
agree on the same pair of numbers.

</details>

---

## When you need exactness

When base-10 exactness matters, step off hardware floats onto a software numeric type:

- `Decimal` — exact base-10 arithmetic, within a configurable precision (default 28
  significant digits). Construct it from a string; building from a float imports the
  float's error:

  ```python
  Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True
  Decimal(0.1)  + Decimal(0.2)  == Decimal("0.3")     # False  <- the trap
  ```

  Reach for it for money and anywhere a human expects base-10 decimal rounding.
- `Fraction` — exact rationals of unbounded precision:

  ```python
  Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10)   # True
  ```

  Reach for it when you need true rational arithmetic — values like `1/3` that no finite
  decimal can hold.
- Integer cents — for money you can often skip non-integer types entirely: store amounts as
  a whole number of cents (or other smallest units) in an `int`, do all arithmetic in `int`
  (always exact, no precision limit), and divide by 100 only when formatting for display.

**The trade-off (precision vs. performance).** Both are implemented in software (the
`decimal`/`fractions` libraries, not the hardware FPU), so they carry a real CPU and memory
cost — often an order of magnitude or more slower than native floats. The two scale
differently: `Decimal`'s overhead is a roughly constant factor, while
`Fraction`'s grows with the length of the computation. Reach for these where correctness
demands it, not by default.

<details>
<summary><b><code>Decimal</code> vs <code>Fraction</code>: exact about different things</b></summary>

Both avoid binary rounding, but they're exact about different things — and "exact" has a
limit for one of them.

* `Decimal` is exact in base 10, but fixed-precision. Addition, subtraction, and
  multiplication of decimals stay exact, but division rounds at the context precision
  (default 28 significant digits). So `Decimal(1) / Decimal(3)` is `0.3333…` (28 threes),
  not exact — `Decimal` cannot represent `1/3`. Its strength is matching human base-10
  expectations, with a configurable rounding mode (default round-half-to-even).
* `Fraction` is exact for every rational, with no fixed precision — numerator and
  denominator are arbitrary-precision integers, so `1/3` is held perfectly. The cost is
  that denominators grow as you chain operations:
  $\frac{1}{1} + \frac{1}{2} + \dots + \frac{1}{10}$ is already
  `Fraction(7381, 2520)`, and a long computation can balloon the denominator until both
  time and memory suffer. `Decimal`'s overhead is a roughly constant factor; `Fraction`'s
  scales with the length of the computation.

Rule of thumb: money and base-10 reporting → `Decimal`; exact ratios and rational math
(probabilities, exact slopes) → `Fraction`.

</details>

---

## Rounding with `round()`

Python's built-in `round()` uses **round half to even** ("banker's rounding") on genuine
ties:

```python
round(0.5)   # 0
round(1.5)   # 2
round(2.5)   # 2
round(3.5)   # 4
```

`round(2.675, 2) == 2.67` is **not** a tie — it is a representation effect: `2.675` is stored as slightly less than
`2.675`, so `round` sees a value below the midpoint and rounds down regardless of the
tie rule. For guaranteed base-10 rounding, round a `Decimal` instead.

<details>
<summary><b>Why round-half-to-even (the bias argument)</b></summary>

The grade-school rule rounds every tie up ($0.5 \to 1$, $1.5 \to 2$). Over many values
this introduces a small but systematic upward bias, because ties always move in the same
direction. Summing millions of such rounded values inflates the total.

Round half to even removes the bias by sending ties to whichever neighbor is even, so
roughly half go up and half go down:

* `round(0.5) == 0` (0 is even)
* `round(1.5) == 2` (2 is even)
* `round(2.5) == 2` (2 is even)
* `round(3.5) == 4` (4 is even)

This is the IEEE 754 default and Python 3's default for both `round()` and `Decimal`. When
you specifically need round-half-up (some financial/tax rules), use
`Decimal(...).quantize(..., rounding=ROUND_HALF_UP)`.

</details>

---

## Special values

### `nan` — not a number

- **Self-unequal:** `float("nan") != float("nan")` is `True`; `nan` equals nothing,
  including itself. Detect it with `math.isnan`, never `==`.
- **Unordered:** every `<`, `>`, `<=`, `>=` against a `nan` returns `False`. A stray `nan`
  silently corrupts `sorted()` and `max()`, which assume comparisons are decidable.
- **Identity beats value in containers:** the `in` operator and `set`/`dict` keys test
  identity (**same object** in memory) before `==`,
  so the same object is found but a fresh one isn't:

  ```python
  n = float("nan")
  n in [n]                          # True   (same object: identity matches)
  math.isnan(n)                     # True   (the right way)
  float("nan") in [float("nan")]    # False  (distinct objects; == is False)
  {float("nan"), float("nan")}      # a set with TWO elements
  ```

### `inf` — infinity

- **Ordered** (unlike `nan`): greater than any finite value — `float("inf") > 1e308` is
  `True`.
- A too-large literal becomes it silently: `1e400 == float("inf")` is `True`.
- Most arithmetic is well-defined (`inf + 1` is `inf`, `1 / inf` is `0.0`); only
  **indeterminate forms** collapse to `nan` — `inf - inf`, `inf / inf`, `0.0 * inf`.

Both interact with `math.isclose` by its normal rules (§ Comparing floats): each
infinity is close only to itself (`isclose(inf, inf)` is `True`, `isclose(inf, -inf)` is
`False`), and a `nan` is close to nothing, itself included (`isclose(nan, nan)` is `False`).

<details>
<summary><b>How <code>nan</code> and <code>inf</code> are encoded</b></summary>

IEEE 754 reserves one exponent pattern as a flag for special states: when all 11 exponent
bits are `1`, the value isn't a normal number, and the 52 fraction bits say which state
it is:

* `inf`: exponent all `1`s, fraction all `0`s. The sign bit picks $+\infty$ or
  $-\infty$.
* `nan`: exponent all `1`s, fraction nonzero (any bit set).

They use the identical 64-bit layout as `0.1` or `5.0`, which is why `type(float("nan"))` is
`float` — they're ordinary float objects carrying a reserved bit pattern, not a separate
type.

</details>

<details>
<summary><b>Why <code>nan != nan</code>, and how it corrupts sorting and membership</b></summary>

**Self-unequal.** A `nan` marks an undefined result, and IEEE 754 makes it unordered with
everything — every comparison except `!=` returns `False`. The intuition: `inf - inf` and
`inf / inf` both yield `nan`, but they stand for genuinely different undefined quantities, so
calling them "equal" would be meaningless. The consequence: `x == nan` is always `False`, so
`==` can never detect a `nan`. Use `math.isnan(x)`.

**Silent sort corruption.** Because every comparison involving the `nan` returns `False`,
a sort can't place it consistently. CPython's sort algorithm (**Timsort**, the hybrid
merge/insertion sort behind `list.sort` and `sorted`) assumes a total order — if `a < b` is
`False` it treats `b <= a` as true — but a `nan` makes both directions `False`, so it gets
stranded
wherever the comparisons happen to leave it. No error is raised; the list simply comes back
wrong, and where it goes wrong depends on the `nan`'s starting position. `max()` and
`min()` break the same way — `max([nan, 1.0, 2.0, 3.0])` returns `nan` while
`max([1.0, 2.0, 3.0, nan])` returns `3.0`, purely from position.

**Identity beats value in containers.** CPython's equality helper returns `True` immediately
when two operands are the same object (the same address in memory), before it ever
calls `==`. The `in` operator walks the container asking "is this element the same object as,
or `==` to, the target?"; `set` and `dict` do the same to find a key. This guarantees an
object is always found in a container that holds it — even a `nan`, which is not `==` to
itself. So:

* `n in [n]` — the element is `n` (same object); identity matches and `in` returns `True`
  without checking `==`.
* `float("nan") in [float("nan")]` — two distinct objects; identity fails, so `in` falls
  back to `==`, which is `False`. `{float("nan"), float("nan")}` keeps both for the same
  reason: distinct objects that aren't `==` are distinct keys.

**The anti-pattern:** never lean on `n in [...]` (or identity) to find a `nan`. It only works
when you hold the very same object, and a `nan` arriving from a file, an API, or a dataframe
never will. Always use `math.isnan`.

</details>

<details>
<summary><b>Why <code>inf</code> appears, and when it decays to <code>nan</code></b></summary>

**Why it exists.** A double is fixed at 64 bits, so it has a largest finite value,
`sys.float_info.max` $= 1.7976931348623157 \times 10^{308}$. Python's integers grow
without bound by allocating more memory; floats can't. When a value exceeds that ceiling the
result is `inf` rather than a crash — and being ordered "above everything," it compares
greater than any finite number.

**But overflow isn't uniform.** A too-large literal (`1e400`) and basic arithmetic overflow
(`1e308 * 10`, `1e308 + 1e308`) silently produce `inf`. Other operations raise
`OverflowError` instead — notably `**` and many `math` functions (`2.0 ** 2000`,
`math.exp(1000)`). So "too big → `inf`" doesn't hold everywhere.

**When it decays to `nan`.** Ordinary arithmetic on `inf` stays well-defined: `inf + 1` is
`inf`, `inf * 2` is `inf`, `1 / inf` is `0.0`. Only **indeterminate forms** — where math has
no single answer — collapse to `nan`: `inf - inf`, `inf / inf`, `0.0 * inf`. (Note `0 / 0`
does not reach `nan`: it raises `ZeroDivisionError`. The route to `nan` is through `inf`
arithmetic.)

</details>

---

## Integers as floats

- A double represents every integer exactly only up to `2**53` (`9007199254740992`). Beyond
  it, consecutive integers collapse: `float(2**53) == float(2**53 + 1)` is `True`.
- An `int` and an equal-valued `float` share a hash and compare equal, so they are the
  same dict key: `{1: "a", 1.0: "b"}` is `{1: "b"}`.
- PEP 484 makes a similar choice for static typing: an `int` is accepted where a `float` is
  annotated, even though `issubclass(int, float)` is `False` at runtime.

<details>
<summary><b>Why integers collapse past <code>2**53</code></b></summary>

The significand carries 53 bits of precision (52 stored + 1 hidden, from § Why floats are
imprecise). Those 53 bits can hold every whole number from $0$ up to $2^{53} =
9{,}007{,}199{,}254{,}740{,}992$ exactly. The integer $2^{53} + 1$ would need a 54th bit, so
it can't be stored; the FPU rounds it (half-to-even) back down to $2^{53}$. Hence
`float(2**53)` and `float(2**53 + 1)` are the same double, and comparing them is `True`.

Above $2^{53}$, the 52-bit fraction limit forces the exponent to scale up while the
available digits stay fixed. Because the step size between representable floats is
determined by $2^{\text{exponent} - 52}$, the spacing (ULP) widens to
$2^{53-52} = 2$ (allowing only even numbers), then to $2^{54-52} = 4$ (allowing only
multiples of 4), and so on. Any integer that falls between those grid lines literally
cannot exist as a float. Python is forced to round it to the nearest available grid line,
which is why large integer IDs must never be round-tripped through `float`.

</details>

<details>
<summary><b>Why <code>{1: ..., 1.0: ...}</code> collapses to one key</b></summary>

A `dict` finds a key by hash, then confirms with `==`. Python guarantees that objects which
compare equal hash equal, and it extends this across the numeric types: `1 == 1.0` is `True`
and `hash(1) == hash(1.0)`. So when the interpreter builds `{1: "a", 1.0: "b"}` it hashes
`1`, stores `"a"`, then hashes `1.0`, lands on the same bucket, finds `1.0 == 1`, and treats
it as an update — overwriting `"a"` with `"b"`. The result is `{1: "b"}`: one key, the
last value.

PEP 484's typing rule echoes the same idea at the type-checker level — an `int` is accepted
where a `float` is annotated, because every integer is a real number — even though at
runtime `issubclass(int, float)` is `False`. In both the
hashing rule and the typing rule, numerical value is treated as more important than runtime
representation.

</details>

---

## Floor division

`//` floors toward negative infinity, and the
remainder `%` takes the sign of the divisor:

```python
-7.5 // 2     # -4.0   (not -3.0)
-7.5 % 2      #  0.5
 7.5 // 2     #  3.0
```

<details>
<summary><b>Why <code>-7.5 // 2</code> is <code>-4.0</code> and the remainder is positive</b></summary>

The exact quotient of $-7.5 / 2$ is $-3.75$. **Flooring** means taking the greatest integer
not greater than that value — moving toward negative infinity — which is $-4.0$.

Python ties `//` and `%` together by the identity

$$a = b \times (a // b) + (a \bmod b)$$

With $a = -7.5$, $b = 2$, and $a // b = -4.0$: $-7.5 = 2 \times (-4.0) + r = -8.0 + r$, so
$r = 0.5$. Because flooring made the quotient "too negative," the remainder must be positive
to balance the identity — which is why `%` carries the sign of the divisor. (The result is a
`float` because an operand is a `float`.)

</details>

---

## Gotchas & practical upshots

### Gotchas

| Surprise                                                | Why it happens                                                                                                                                                     | Fix                                                                                                               |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| `0.1 + 0.2 == 0.3` is `False`                           | `0.1`, `0.2`, and `0.3` have denominators that are not powers of 2, so each is rounded to the nearest double and the two errors do not cancel to the stored `0.3`. | Compare computed floats with `math.isclose`, not `==`.                                                            |
| `math.isclose(0.0, x)` is `False` for every nonzero `x` | The relative buffer is $\text{rel\_tol} \times \lvert x \rvert$, which is smaller than $\lvert x \rvert$ itself.                                                   | Pass an `abs_tol` when either side can be zero, e.g. `math.isclose(0.0, x, abs_tol=1e-9)`.                        |
| `Decimal(0.1)` is not `0.1`                             | The `float` `0.1` already carries binary error, and building a `Decimal` from it copies that error.                                                                | Construct from a string: `Decimal("0.1")`.                                                                        |
| `round(2.675, 2)` is `2.67`, not `2.68`                 | `2.675` is stored just below the midpoint, so it is not a tie and rounds down.                                                                                     | Round a `Decimal("2.675")` for true base-10 rounding.                                                             |
| `nan` breaks `==`, `in`, `sorted()`, and `max()`        | `nan` is self-unequal and unordered, and containers match by identity before `==`.                                                                                 | Detect with `math.isnan`; do not use `==`, `in`, or identity, and screen out `nan` before sorting.                |
| A running total in a `+=` loop drifts                   | Each addition re-rounds, and the errors accumulate. Summing `0.1` ten times by hand gives `0.9999999999999999`.                                                    | Use `math.fsum(values)` for a correctly rounded sum.                                                              |
| Large integers lose precision as `float`                | Past `2**53`, the double grid is coarser than $1$.                                                                                                                 | Keep big IDs and counters as `int`; do not round-trip them through `float`.                                       |
| Overflow is non-uniform                                 | Literals and basic arithmetic give `inf` silently, but `**` and many `math` functions raise `OverflowError`.                                                       | Do not assume "too big" always becomes `inf`; guard with `try`/`except OverflowError` where operations can raise. |

### Reach for

- **Equality of computed floats →** `math.isclose` (set `abs_tol` if a side may be zero).
- **Exact money / base-10 reporting →** `decimal.Decimal` (build from strings), or integer
  cents.
- **Exact rationals (`1/3`, exact slopes, probabilities) →** `fractions.Fraction`.
- **Correctly-rounded sum of many floats →** `math.fsum`.
- **Detect `nan` →** `math.isnan` (and `math.isinf` for infinities).
- **Inspect a float →** `decimal.Decimal(x)` for the exact stored value,
  `struct.pack('>d', x)` for the raw bits, `math.ulp(x)` for the local spacing.
- **Lossless serialization →** `repr(x)` round-trips: `float(repr(x)) == x`.

---

## Cheat sheets

### Type selection

| Type       | Exact about                                       | Cost                                    | Reach for                         |
| ---------- | ------------------------------------------------- | --------------------------------------- | --------------------------------- |
| `float`    | fractions with power-of-2 denominators (≤53 bits) | hardware-fast                           | general numeric work              |
| `Decimal`  | base-10 to a fixed precision (28)                 | software; ~constant factor slower       | money, human base-10 rounding     |
| `Fraction` | every rational, unbounded                         | software; grows with computation length | exact ratios, `1/3`, exact slopes |

### Special-value bit patterns (binary64)

| Value          | Sign | Exponent (11 bits)   | Fraction (52 bits) |
| -------------- | ---- | -------------------- | ------------------ |
| Normal         | 0/1  | not all-0, not all-1 | any                |
| Subnormal / ±0 | 0/1  | all `0`              | nonzero / all `0`  |
| `±inf`         | 0/1  | all `1`              | all `0`            |
| `nan`          | 0/1  | all `1`              | nonzero            |

### `math.isclose` parameters

| Parameter | Default | Meaning                                                                            |
| --------- | ------- | ---------------------------------------------------------------------------------- |
| `rel_tol` | `1e-9`  | relative tolerance, scaled by $\max(\lvert a \rvert, \lvert b \rvert)$ (symmetric) |
| `abs_tol` | `0.0`   | absolute floor; required when either argument may be `0.0`                         |

Test applied: $|a - b| \le \max(\text{rel\_tol} \times \max(|a|, |b|),\ \text{abs\_tol})$.
