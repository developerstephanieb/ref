# Asymptotic Notation

The language for describing how an algorithm's cost grows with input size — $O$, $\Theta$, $\Omega$ — and the precision traps around them. This covers the notation and growth classes themselves; deriving a bound from loops or recurrences (the [Master Theorem](../complexity_from_code/README.md)) and [amortized analysis](../amortized_analysis/README.md) are separate topics. Each section's dominance claims are verified empirically in the correspondingly-named function in [mechanics.py](./mechanics.py).

---

## Why Asymptotics

We evaluate algorithms by their **order of growth** — how resource utilization (time or space) scales with respect to the input size $n$. Asymptotic analysis deliberately abstracts away two variables:

1. **Constant environmental factors:** hardware constraints, language overhead. 
2. **Performance on trivially small inputs:** A claim like "$O(n^2)$" describes only the algorithm's dominant trajectory for **sufficiently large $n$** (formally, $\forall n \ge n_0$).

In practice, an asymptotically slower algorithm can be the superior choice for small, bounded datasets. Comparing $100n$ against $n^2$, the quadratic curve is strictly faster for every $n < 100$, only losing its edge once we pass the crossover point at $n_0 = 100$.

```python
n = 50:   100n = 5000    n² = 2500     # n² is faster here
n = 200:  100n = 20000   n² = 40000    # n² is slower here
```

<details>
<summary><b>The role of n<sub>0</sub>, and why we drop constants</b></summary>

Wall-clock time and exact instruction counts are unreliable metrics because they are entirely dependent on the execution environment — hardware, compiler optimizations, and caching layers. Asymptotic analysis deliberately abstracts these away. If two algorithms process a linear scan but one has a 1000x heavier memory footprint per item, both are still mathematically $\Theta(n)$. We drop the constant factor $c$ because it represents hardware and implementation details, not the fundamental trajectory of the algorithm's scaling behavior.

An algorithm's behavior on small inputs is often heavily skewed by constant overhead or lower-order terms. The threshold $n_0$ is the formal inflection point where we legally discard that noise. By defining our bounds strictly for $n \ge n_0$, we admit that an asymptotically slower algorithm might win on tiny datasets, but we guarantee our bound holds true as the input scales toward infinity.

**Takeaway:** Asymptotic notation evaluates the intrinsic mathematical efficiency of the algorithmic design, completely decoupled from the machine it runs on.

</details>

---

## Big-O — The Asymptotic Upper Bound

$f(n) = O(g(n))$ indicates that an algorithm's resource utilization $f$ grows **no faster than** a designated bound $g$, up to a constant factor, as the input scales. Formally:

$$f(n) = O(g(n)) \iff \exists\, c > 0,\ n_0 > 0 \ \text{ s.t. } \ 0 \le f(n) \le c \cdot g(n) \ \text{ for all } n \ge n_0$$

This formula leverages two critical parameters to abstract away real-world noise:

* **The threshold ($n_0$):** Absorbs lower-order terms that dominate on small data but become mathematically irrelevant as $n$ scales toward infinity.
* **The constant multiplier ($c$):** Absorbs fixed overhead like language latency, hardware constraints, and non-dominant operations.

In practical terms: Past a definitive crossover threshold ($n_0$), the algorithm's resource utilization ($f(n)$) is strictly upper-bounded by the scaled function ($c \cdot g(n)$). 

Crucially, Big-O is strictly an **asymptotic upper bound**, not a synonym for "worst-case runtime." A bound caps a mathematical function, whereas a case (best/average/worst) dictates which input distribution we are evaluating. An upper bound can be mathematically true but practically loose (e.g., stating $n = O(n^2)$ is valid, just uninformative).

*Note on notation:* The $=$ in $f(n) = O(g(n))$ is an accepted abuse of notation. $O(g)$ defines a **set** of functions, so the relation is strictly one-directional ($f \in O(g)$). You can write $3n = O(n^2)$, but never $O(n^2) = 3n$.

<details>
<summary><b>Why "Big-O = worst case" is a category error</b></summary>

Conflating Big-O with the worst-case scenario is a frequent pitfall. They answer fundamentally different questions:

* **Case (Best / Average / Worst):** Defines the input distribution you are analyzing.
* **Bound ($O$, $\Theta$, $\Omega$):** Describes the asymptotic geometry of the resulting cost function.

Because these axes are completely independent, **you can apply any bound to any case**. For instance, the best-case input for Insertion Sort is an already-sorted array, which yields a linear cost function. You can tightly bound this specific case as $\Theta(n)$, establish a lower floor as $\Omega(1)$, or place a loose ceiling on it as $O(n^2)$. The bound mathematically limits the function's growth; it does not dictate what the input data looks like.

</details>

---

## Big-Omega — The Asymptotic Lower Bound

$\Omega$ is the mathematical dual to $O$: it defines an **asymptotic lower bound**, acting as a strict floor on growth.

$$f(n) = \Omega(g(n)) \iff \exists\, c > 0,\ n_0 > 0 \ \text{ s.t. } \ 0 \le c \cdot g(n) \le f(n) \ \text{ for all } n \ge n_0$$

In practical terms: Past a definitive threshold ($n_0$), the algorithm's resource utilization ($f(n)$) is strictly lower-bounded by the scaled function ($c \cdot g(n)$). Therefore, $f(n) = \Omega(g(n))$ asserts that $f$ grows **at least as fast as** $g$.

Just like Big-O, a Big-Omega bound can be mathematically true but practically loose (e.g., stating $n^2 = \Omega(n)$ is mathematically valid, just uninformative).

<details>
<summary><b>Formalizing a Big-Omega (&Omega;) proof</b></summary>

To formally prove that a function like $f(n) = \frac{1}{2}n^2 - 3n$ is $\Omega(n^2)$, we must identify a scaled baseline that creates a permanent floor beneath our function as $n \to \infty$.

By definition, we need to prove $c \cdot g(n) \le f(n) \forall n \ge n_0$. We deliberately select $c = \frac{1}{4}$, a scaling factor that is strictly smaller than the leading coefficient of $\frac{1}{2}$), and solve for the exact inflection point ($n_0$) where this floor takes effect:

$$\frac{1}{4}n^2 \le \frac{1}{2}n^2 - 3n$$

$$0 \le \frac{1}{4}n^2 - 3n$$

$$3n \le \frac{1}{4}n^2$$

Divide both sides by $n$ (valid since input size $n > 0$):
$$3 \le \frac{1}{4}n$$

$$12 \le n$$

This algebraic reduction mathematically guarantees that once the input size reaches $12$ (our $n_0$), the inequality holds infinitely. The bound $\frac{1}{4}n^2$ establishes a permanent floor beneath the algorithm's growth trajectory from that point forward.

</details>

---

## Big-Theta — The Tight Bound

$f(n) = \Theta(g(n))$ asserts that $f$ is bounded **both above and below** by constant multiples of $g$ - it grows at the same asymptotic rate.

$$f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \ \textbf{and} \ f(n) = \Omega(g(n)),$$

Equivalently, $\exists\, c_1, c_2, n_0 > 0$ such that:

$$c_1 g(n) \le f(n) \le c_2 g(n) \ \text{ for all } n \ge n_0$$

In practical terms: Past our definitive threshold ($n_0$), the algorithm's resource utilization ($f(n)$) is strictly bounded within a constant-factor envelope, bounded between a lower-bound floor ($c_1 \cdot g(n)$) and an upper-bound ceiling ($c_2 \cdot g(n)$).

Favor $\Theta$ whenever you can prove both bounds. It is the most precise and transparent characterization of the algorithm's scaling behavior. If you can identify both a floor constant ($c_1$) and a ceiling constant ($c_2$), report $\Theta$.

<details>
<summary><b>Formalizing a Big-Theta (&Theta;) proof</b></summary>

To formally prove that the function $f(n) = 3n^2 + 50n + 200$ is exactly $\Theta(n^2)$, we must constrain it within an asymptotic envelope — between a floor function ($c_1 \cdot n^2$) and a ceiling function ($c_2 \cdot n^2$). We prove the function never escapes these bounds as $n \to \infty$.

Divide the function by $n^2$ to isolate the constants ($c_1$ and $c_2$):

$$\frac{3n^2 + 50n + 200}{n^2} = 3 + \frac{50}{n} + \frac{200}{n^2}$$

Next, establish an inflection threshold ($n_0$). We deliberately select $n_0 = 10$ simply because it resolves our fractional terms into clean integers for evaluation:

* **The Ceiling ($c_2$):** Plugging in $n_0 = 10$, the ratio evaluates to $3 + 5 + 2 = 10$. As $n$ grows infinitely larger than 10, the fractional terms strictly shrink, meaning the aggregate ratio will never exceed 10. To safely guarantee an upper bound envelope, we set $c_2 = 11$.
* **The Floor ($c_1$):** As $n \to \infty$, $\frac{50}{n} \to 0$ and $\frac{200}{n^2} \to 0$. Because $n$ represents input size (which is always positive), the ratio inherently never drops below the leading coefficient. We set the floor constant to $c_1 = 3$.

Reassembling the inequality with these derived constants yields our formal bounds for all $n \ge 10$:

$$3n^2 \le f(n) \le 11n^2$$

Having definitively established both the upper and lower bounds, we conclude $f(n) = \Theta(n^2)$. 

This mathematical convergence formally illustrates why **lower-order terms** ($50n$ and $200$) are discarded in asymptotic analysis: their impact becomes strictly negligible at scale.

</details>

---

## little-o and little-omega — The Strict Bounds

While Big-$O$ and Big-$\Omega$ define inclusive bounds (allowing for asymptotic tightness, analogous to $\le$ and $\ge$), the strict variants, little-$o$ and little-$\omega$, enforce **strict inequality** ($<$ and $>$).

Rather than relying on constant multipliers, strict bounds are formally evaluated using limit calculus as $n \to \infty$:

$$f(n) = o(g(n)) \iff \lim_{n \to \infty} \frac{f(n)}{g(n)} = 0, \qquad f(n) = \omega(g(n)) \iff \lim_{n \to \infty} \frac{f(n)}{g(n)} = \infty.$$

In practical terms:
* **little-$o$ (Strict Upper Bound)**: $f(n) = o(g(n))$ dictates that $f$ is strictly dominated by $g$. The resource utilization gap widens infinitely without bound, guaranteeing the bound is never tight ($f(n) \ne \Theta(g(n))$).
* **little-$\omega$ (Strict Lower Bound)**: The inverse relation; $f(n) = \omega(g(n))$ dictates that $f$ strictly dominates $g$.

Note on hierarchy: When establishing a growth-class ladder using the strict domination operator ($a \ll b$), it is a precise mathematical assertion that $a = o(b)$, meaning $a$ is strictly faster than $b$.

---

## Simplification — Asymptotic Reduction Axioms

Converting an exact instruction count into an asymptotic class relies on three fundamental reduction axioms:

1. **Drop constant factors:** $5n^2 = \Theta(n^2)$. The scaling factor $c$ in the formal definition mathematically absorbs these environmental constants.
2. **Drop lower-order terms (within a single variable):** $n^2 + n = \Theta(n^2)$. The $n$ is dominated by the $n^2$ and becomes mathematically irrelevant as the system scales.
3. **Abstract standalone logarithmic bases:** $\log_2 n$ and $\ln n$ differ strictly by a constant scalar ($1/\ln 2 \approx 1.4427$). In asymptotic notation, we omit the base and write $\log n$.

Two edge cases when reducing complexity bounds:

- **Independent variables do not collapse.** $O(n + m)$ cannot be reduced to $O(n)$. There is no constant $c$ that guarantees $n + m \le c\,n$ if $m$ is allowed to scale independently. Graph complexities like $O(V + E)$ must permanently retain both terms.
- **Log base matters inside an exponent.** While a standalone log base is a free constant, $n^{\log_2 n}$ and $n^{\log_3 n}$ belong to different growth classes. A base buried in an exponent dictates the power scaling, not just a scalar coefficient.

<details>
<summary><b>Why change-of-base is a constant, and why the exponent is the exception</b></summary>

The mathematical property allowing us to drop standalone log bases is the change-of-base identity:

$$\log_b n = \dfrac{\log_k n}{\log_k b}$$ 

For any two fixed bases $b, k$, the factor $1/\log_k b$ is strictly a constant scalar. Therefore, $\log_b n$ and $\log_k n$ differ only by that constant — precisely the $c$ factor that Big-$O$ discards. 

The exponent is an exception because the constant ceases to act as a coefficient.
Using logarithmic properties, $n^{\log_2 n} = n^{(\ln n)/\ln 2}$. A constant within an exponent rescales the power, not the value (e.g., the difference between $n^c$ and $n^{2c}$). These represent different mathematical classes. 

**Notation Pitfall:** Be highly deliberate with superscript notation. $\log^2 n$ is universally evaluated as $(\log n)^2$. It is not equivalent to $\log(\log n)$, or $\log(n^2)$ which simplifies to $2\log n = \Theta(\log n)$. They all belong to entirely different complexity classes.

</details>

---

## Composition — Combining the Cost of Parts

After isolating the resource costs of individual code blocks, we combine the aggregate algorithmic complexity using three structural combinators.

- **Sequence execution (addition → max)** Code blocks executing consecutively sum their bounds, yielding $O(f + g)$, which mathematically reduces to $O(\max(f, g))$. For example, an $O(n)$ preprocessing pass followed by an $O(n^2)$ computation totals $\Theta(n^2)$ because the strictly smaller term is discarded.
- **Nested iteration (multiplication):** A subroutine or loop executing $g$ operations embedded within a loop of $f$ iterations scales multiplicatively, bounding at $O(f \cdot g)$. An $O(n)$ iterative loop wrapping an $O(n^2)$ internal operation structurally guarantees an $O(n^3)$ cost.
- **Conditional branching (branch → max):** For `if/else` control flows diverging into paths of cost $f$ and $g$, the worst-case execution strictly bounds to the maximum of the branches, $O(\max(f, g))$. You account for the most computationally expensive routing path, never their combined sum.

The habit is accurately parsing the control flow architecture. Two loops executing sequentially add together (reducing to the maximum), while the exact same two loops nested multiply. The structural arrangement strictly dictates the combinator applied.

---

## The Growth-Class Hierarchy

The asymptotic growth hierarchy orders complexity classes from most to least efficient. We use the $\ll$ operator to formally denote that a class is **strictly dominated by** the next ($a \ll b \implies a = o(b)$).

$$1 \ll \log n \ll \sqrt{n} \ll n \ll n \log n \ll n^2 \ll n^3 \ll 2^n \ll n!$$

Standard nomenclature for these complexity classes includes:

* **Constant:** $O(1)$
* **Logarithmic:** $O(\log n)$
* **Sublinear:** $O(\sqrt{n})$
* **Linear:** $O(n)$
* **Linearithmic:** $O(n \log n)$
* **Polynomial:** $O(n^c)$ (inclusive of **quadratic** $O(n^2)$ and **cubic** $O(n^3)$)
* **Exponential:** $O(c^n)$
* **Factorial:** $O(n!)$

<details>
<summary><b>Formalizing the hierarchy limit arguments</b></summary>

To prove a strict separation where $a$ is strictly dominated by $b$ ($a \ll b$), we mathematically assert that the ratio $a/b \to 0$ as the input $n \to \infty$. 

- **Linearithmic is strictly dominated by Quadratic ($n \log n \ll n^2$):** Evaluating the limits confirms that $O(n \log n)$ is a fundamentally better class than $O(n^2)$. Specifically, $\frac{n \log n}{n^2} = \frac{\log n}{n} \to 0$.
- **Logarithmic and polylog factors lose to any polynomial power:** $\log n \ll \sqrt{n}$, and even $(\log n)^3 \ll n$ — so a stray log factor never changes the polynomial class ($n \log n \ll n^{1.5}$).
- **Polynomial is strictly dominated by Exponential ($n^c \ll 2^n$):** The ratio $n^c / 2^n \to 0$ for any fixed polynomial degree $c$. The exponential denominator accelerates so violently that it will permanently suppress the polynomial numerator as $n$ scales.
- **Exponential bases are strictly decisive:** This is why we drop bases for logarithms but keep them for exponents. $2^n / 3^n = (2/3)^n \to 0$, which proves $2^n \ll 3^n$. They represent entirely different mathematical trajectories.
- **Factorial strictly dominates Exponential ($2^n \ll n!$):** Utilizing Stirling's approximation ($n! \sim \sqrt{2\pi n}\,(n/e)^n$), we can formally prove $2^n / n! \to 0$, demonstrating that factorial time is fundamentally worse than any fixed-base exponential.

</details>

---

## Case vs. Bound vs. Amortized — The Three Axes

A ubiquitous trap in algorithmic analysis is conflating the mathematical *bound* with the input *case*, or incorrectly categorizing "amortized" as just a fourth data case. These are three fundamentally orthogonal dimensions of analysis:

* **Case (The Input Distribution):** Dictates *which specific data state* is being evaluated in an isolated event (e.g., Best, Average, Worst). This establishes the underlying cost function.
* **Bound (The Mathematical Envelope):** Dictates *how* we mathematically constrain that resulting cost function (e.g., Upper $O$, Tight $\Theta$, Lower $\Omega$).
* **Amortized (The Sequence):** Evaluates the mathematically guaranteed average cost across a *deterministic timeline* of interconnected operations, entirely devoid of probability.

Because Case and Bound are independent, **any bound can sit on any case**. 
* **Insertion Sort:** Its best-case input (an already-sorted array) yields a linear cost function, tightly bounded as $\Theta(n)$. Its worst-case input (reversed) is bounded as $\Theta(n^2)$.
* **Quicksort:** Best and average cases are tightly bounded at $\Theta(n \log n)$, while the worst-case scenario degrades to $\Theta(n^2)$. Therefore, asking "What is the Big-O of Quicksort?" is technically an underspecified prompt until the input distribution (the case) is explicitly named.

While Case and Bound analyze single operations in isolation, Amortized analysis evaluates systemic scaling. For example, appending to a dynamic array has an isolated worst-case bound of $O(n)$, but an amortized worst-case bound of strictly $O(1)$.

<details>
<summary><b>Isolation vs. sequence (the dynamic array)</b></summary>

If the **Case** axis dictates *which specific input* you are analyzing, the **Amortized** axis dictates *how many operations* you are evaluating over time. 

**Isolation vs. Sequence**
* **Worst-case (Isolation):** Evaluates a single, isolated event and assumes the absolute maximum cost for an adversarial input. 
* **Average-case (Isolation):** Evaluates a single, isolated event but factors in probability over an input distribution. It asks: *"If I run this one operation many times on random data, what is the mathematically expected average?"*
* **Amortized (Sequence):** Evaluates a continuous, connected sequence of operations. It relies strictly on state sequence and deterministic mathematical guarantees.

**The Dynamic Array Example**
When you append an item to a dynamic array, the operation is usually instant ($O(1)$). However, when the array reaches capacity, an append triggers a resize:
1. The system allocates a new, doubled memory block.
2. It copies $n$ existing elements into the new array.
3. It inserts the new element.

Because copying takes $n$ steps, that specific, isolated event has a worst-case cost of $O(n)$.

This is where amortized analysis paints the true picture . Because the expensive $O(n)$ resize doubled the capacity, it mathematically guarantees that the next $n$ append operations will be cheap $O(1)$ operations. The heavy cost of the resize is "paid for" — or *amortized* — across that subsequent sequence. 

When you divide the total structural cost ($3n$) by the number of operations in the sequence ($n$), the average mathematically simplifies strictly to $O(1)$. 

</details>

---

## Gotchas

| Anti-Pattern                                                    | The Underlying Fallacy                                                                                                            | The Fix                                                                                                                                                                                               |
| :-------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **"Big-$O$ means the worst case"**                              | Conflating the mathematical boundary ($O$ caps a function) with the input distribution (case picks the data state).               | Explicitly separate the axes: "The worst-case input scales at $\Theta(n^2)$".                                                                                                                         |
| **Reporting $O(n^2)$ for a tight result**                       | Using a strictly upper-bound ($O$) when a two-sided mathematical proof exists.                                                    | Default to precision. If both floor ($c_1$) and ceiling ($c_2$) are proven, report $\Theta$.                                                                                                          |
| **Collapsing multivariate bounds (e.g., $O(n + m)$ to $O(n)$)** | Assuming independent variables scale proportionately. No scalar $c$ guarantees $n + m \le c \cdot n$ if $m$ scales independently. | Retain all independent variables. Graph traversal complexities like $O(V + E)$ must keep both terms.                                                                                                  |
| **Treating a standalone log's base as significant**             | Failing to recognize the change-of-base formula yields a constant scalar, which asymptotic limits discard.                        | Abstract the base entirely ($\log n$)—*unless* it resides within an exponent, where it dictates the growth class.                                                                                     |
| **Confusing $\log^2 n$, $\log(n^2)$, and $\log\log n$**         | Treating distinct mathematical log operations as interchangeable notation.                                                        | $\log^2 n$ evaluates as $(\log n)^2$. Do not confuse it with $\log(\log n)$, or $\log(n^2)$ which simplifies to $2\log n = \Theta(\log n)$. They all belong to entirely different complexity classes. |  | **"A higher Big-$O$ is always objectively slower"** | Ignoring the formal threshold ($n_0$). Asymptotic limits describe scaling toward infinity, not the absolute cost on micro-datasets. | Acknowledge crossover points. An $O(n^2)$ design might strictly outperform an $O(n)$ design on small, bounded arrays. |
| **Adding the cost of an `if/else` branch's paths**              | Misapplying the sequential combinator to a diverging control flow. A branch executes *one* path.                                  | The worst-case cost of an `if/else` block strictly bounds to the maximum of the diverging paths.                                                                                                      |
| **Viewing "amortized" as a fourth data case**                   | Amortized is guarantee over an operation sequence, not over an input distribution.                                                | Treat amortized analysis as its own axis: the guaranteed average cost across a *deterministic sequence* of operations.                                                                                |

---

## Reference

### Strategic Heuristics (What Notation to Reach For)

| Engineering Objective                         | Notation to Reach For                        | Rationale                                                                                    |
| :-------------------------------------------- | :------------------------------------------- | :------------------------------------------------------------------------------------------- |
| **Reporting a tightly constrained function**  | **$\Theta$** (Big-Theta)                     | It is the precise and honest statement of a tight result.                                    |
| **Establishing a guaranteed scaling ceiling** | **$O$** (Big-$O$)                            | Used when you only need to prove an algorithm will grow *no faster than* a designated limit. |
| **Establishing a theoretical minimum floor**  | **$\Omega$** (Big-Omega)                     | Used to assert that a process will take *at least* a certain amount of time.                 |
| **Asserting strict algorithmic superiority**  | **$o$ / $\omega$** (little-o / little-omega) | Used to assert *strict* separation.                                                          |

### Notation Summary

| Notation            | Engineering Definition                         | Formal Constraint                          | Limit Calculus                               | Analogy |
| :------------------ | :--------------------------------------------- | :----------------------------------------- | :------------------------------------------- | :------ |
| **$f = O(g)$**      | **Asymptotic Upper Bound** (Ceiling)           | $\exists c, n_0:\ f(n) \le c\,g(n)$        | $\limsup f/g < \infty$                       | $\le$   |
| **$f = \Omega(g)$** | **Asymptotic Lower Bound** (Floor)             | $\exists c, n_0:\ f(n) \ge c\,g(n)$        | $\liminf f/g > 0$                            | $\ge$   |
| **$f = \Theta(g)$** | **Asymptotic Tight Bound** (Envelope)          | $O(g)$ **and** $\Omega(g)$                 | $0 < \liminf f/g$ and $\limsup f/g < \infty$ | $=$     |
| **$f = o(g)$**      | **Strict Upper Bound** (Strictly dominated by) | $\forall c\, \exists n_0:\ f(n) < c\,g(n)$ | $\lim f/g = 0$                               | $<$     |
| **$f = \omega(g)$** | **Strict Lower Bound** (Strictly dominates)    | $\forall c\, \exists n_0:\ f(n) > c\,g(n)$ | $\lim f/g = \infty$                          | $>$     |

---

### Growth-Class Ladder

| Class          | Nomenclature           | Scalability     | Example Algorithm           | $n=10$          | $n=100$            | $n=1000$            |
| :------------- | :--------------------- | :-------------- | :-------------------------- | :-------------- | :----------------- | :------------------ |
| **$1$**        | Constant               | **Excellent**   | Hash map lookup             | $1$             | $1$                | $1$                 |
| **$\log n$**   | Logarithmic            | **Excellent**   | Binary search               | $3.3$           | $6.6$              | $10$                |
| **$\sqrt{n}$** | Sublinear              | **Good**        | Primality trial division    | $3.2$           | $10$               | $32$                |
| **$n$**        | Linear                 | **Good**        | Array scan                  | $10$            | $100$              | $1000$              |
| **$n\log n$**  | Linearithmic           | **Fair**        | Mergesort                   | $33$            | $664$              | $9970$              |
| **$n^2$**      | Polynomial (Quadratic) | **Poor**        | Insertion sort (worst case) | $100$           | $10^4$             | $10^6$              |
| **$n^3$**      | Polynomial (Cubic)     | **Very Poor**   | Naive matrix multiplication | $10^3$          | $10^6$             | $10^9$              |
| **$2^n$**      | Exponential            | **Intractable** | Subset enumeration          | $\approx 10^3$  | $\approx 10^{30}$  | $\approx 10^{301}$  |
| **$n!$**       | Factorial              | **Intractable** | Brute-force permutations    | $3.6\times10^6$ | $\approx 10^{158}$ | $\approx 10^{2568}$ |

---

### Simplification Rules (Reduction Axioms)

| Expression                               | Simplifies to    | Asymptotic Reduction Axiom                                                  |
| :--------------------------------------- | :--------------- | :-------------------------------------------------------------------------- |
| **$5n^2$**                               | $\Theta(n^2)$    | **Eliminate constant coefficients**                                         |
| **$n^2 + n$**                            | $\Theta(n^2)$    | **Discard strictly dominated terms** (within a single variable)             |
| **$\log_2 n$**                           | $\Theta(\log n)$ | **Abstract standalone logarithmic bases**                                   |
| **$n + m$**                              | $O(n + m)$       | **Multivariate constraints do not collapse**                                |
| **$V + E$**                              | $O(V + E)$       | **Multivariate constraints do not collapse**                                |
| **$n^{\log_2 n}$** vs **$n^{\log_3 n}$** | Distinct classes | **Bases matter inside exponents** (rescales the power, not the coefficient) |

---

### Bound × Case Matrix (Quicksort)

| Case *(The Input Distribution)* | Tight Bound *(The Mathematical Envelope)* | Data State Condition                                                          |
| :------------------------------ | :---------------------------------------- | :---------------------------------------------------------------------------- |
| **Best-Case**                   | $\Theta(n\log n)$                         | Ideal data state yielding balanced partitions at every level                  |
| **Average-Case**                | $\Theta(n\log n)$                         | Probabilistic expected state using random pivots over the input distribution  |
| **Worst-Case**                  | $\Theta(n^2)$                             | Adversarial data state (e.g., already-sorted input paired with a naive pivot) |