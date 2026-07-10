Q: Why use asymptotic notation instead of counting exact operations or timing code?
A: Asymptotic notation isolates the order of growth — how resource cost scales as input size n increases — independent of hardware, language overhead, or constant factors. Because exact timings depend on the environment, asymptotic analysis abstracts them away to focus on intrinsic algorithmic efficiency. "Asymptotic" means the bound applies only after a crossover threshold (`n_0`), describing the trajectory as data scales to infinity (tail), not on trivially small inputs. Consequently, an asymptotically slower algorithm (like `n^2`) can strictly outperform an asymptotically superior one (like `100n`) on small datasets below `n_0`.
TAGS: complexity asymptotic_notation foundations concept
---
Q: Two algorithms are both Θ(n), but one does ~1000× the work per element. Same class? Equally fast?
A: Same class, not equally fast. Both scale linearly so they share the Θ(n) class, but the Θ bound discards the constant factor by design. The heavier algorithm runs ~1000× slower on every input, with no crossover point. A flat, op-count ratio `1000n / n = 1000` is the mathematical signature of a constant gap. "Both Θ(n)" means "both scale the same," not "interchangeable" — constants are real, just invisible to the class.
TAGS: complexity asymptotic_notation foundations gotcha
---
Q: What is the formal definition of `f(n) = O(g(n))`?
A: It defines an asymptotic upper bound. It dictates that f grows no faster than g, up to a constant factor. Formally: There exists constants c > 0 and n_0 > 0 such that 0 <= f(n) <= c * g(n) for all n >= n_0. The bound may be loose (e.g., n = O(n^2) is mathematically true), and the `=` sign is an accepted abuse of notation for set membership (f ∈ O(g)).
TAGS: complexity asymptotic_notation bounds concept
---
Q: What is the formal definition of `f(n) = Ω(g(n))`?
A: It defines an asymptotic lower bound, acting as the mathematical mirror to Big-O. It dictates that f grows at least as fast as g. Formally: There exists constants c > 0 and n_0 > 0 such that 0 <= c * g(n) <= f(n) for all n >= n_0. Like Big-O, this floor can be practically loose (e.g., n^2 = Ω(n) is true).
TAGS: complexity asymptotic_notation bounds concept
---
Q: What does `f(n) = Θ(g(n))` mean, and when may you write it?
A: It defines an asymptotic tight bound, meaning f is bounded both above and below by constant multiples of g. Equivalently, f = O(g) AND f = Ω(g). Formally: There exists constants c_1, c_2, n_0 > 0 such that c_1 * g(n) <= f(n) <= c_2 * g(n) for all n >= n_0. You should only write Θ when you have explicitly proven both bounds - if you can name both c_1 and c_2. Prefer Θ over O when the bound is tight, as writing O understates the precision of the proof.
TAGS: complexity asymptotic_notation bounds concept
---
Q: What do little-o and little-omega mean, in limit form?
A: They are strict mathematical cousins of O and Ω. 
- little-o (strict upper bound): f = o(g) iff lim (f/g) = 0 as n→∞. It dictates f is strictly dominated by g. The gap widens without bound, so the bound is never tight, f != Θ(g).
- little-omega (strict lower bound): f = ω(g) iff lim (f/g) = ∞ as n→∞.
 When building a groth ladder, the shorthand notation `a << b` is the mathematical assertion that a = o(b).
TAGS: complexity asymptotic_notation bounds concept
---
Q: What are the three simplification rules that reduce an exact op-count to an asymptotic class?
A: (1) Drop constant factors: `5n^2 = Θ(n^2)`. (2) Drop lower-order terms within a single variable: `n^2 + n = Θ(n^2)`. (3) Abstract stand-alone logarithmic bases: A change of base yieldds a constant scalar, so write `log n` with no base. 
Exceptions: Independent variables don't collapse (`n+m` stays `n+m`), and log bases inside an exponent dictate the growth class, so they cannot be dropped.
TAGS: complexity asymptotic_notation simplification concept
---
Q: How do you compose the cost of sequential code, nested loops, and an if/else branch?
A: 
- Sequence (A then B): Add, then keep the dominant term — `O(f+g) = O(max(f,g))`. Two separate loops costing `O(n)` and `O(n^2)` yield `O(n^2)`
- Nesting (B inside A's loop): Multiply — `O(f*g)`. An `O(n)` wrapping `O(n^2)` is `O(n^3)`.
- Branch (if/else with arms f and g): Take the max — worst case is `O(max(f,g))`, because execution takes only once path.
TAGS: complexity asymptotic_notation composition concept
---
Q: State the growth-class hierarchy from slowest- to fastest-growing, with canonical names.
A: 1 << log n << √n << n << n log n << n² << n³ << 2ⁿ << n!. 
Names: constant O(1), logarithmic O(log n), sublinear O(√n), linear O(n), linearithmic O(n log n), polynomial (quadratic O(n²), cubic O(n³)), exponential O(2ⁿ), factorial O(n!).
TAGS: complexity asymptotic_notation growth-classes concept
---
Q: "Bound" and "case" are two separate axes. What does each describe?
A: 
- Case (best / average / worst): Selects which input distribution you are analyzing, which establishes the underlying cost function. 
- Bound (O upper / Θ tight / Ω lower): Describes which side you geometrically wrap that resulting cost function from. 
Because they are orthogonal, any bound can sit on any case. For example, 
Insertion Sort's best-case input is tightly Θ(n), but you can mathematically place a loose upper bound of O(n^2) on that exact same best case.
TAGS: complexity asymptotic_notation case-vs-bound concept
---
Q: An algorithm is `O(n^2)`. Does that make it `Θ(n^2)`? When does O differ from Θ?
A: No. O is only a ceiling and may be loose — `n = O(n^2)` is true but `n != Θ(n^2)`. Asserting O(n^2) only guarantees the cost grows no faster than n^2; it does not establish a matching floor. Reporting Θ(n^2) requires also proving both O and Ω.
TAGS: complexity asymptotic_notation bounds gotcha
---
Q: If `f = O(g)`, what does that tell you about `Ω`?
A: Nothing on its own — O and Ω are independent directions. O caps from above, Ω floors from below. For example, `n = O(n^2)` holds but `n = Ω(n^2)` is false. Only when both hold for the same function g do they combine into Θ(g).
TAGS: complexity asymptotic_notation bounds concept
---
Q: Why is "Big-O means the worst case" a category error? Use insertion sort.
A: It conflates the mathematical axis that bounds the function (O) with the distributional axis that selects the input data (case). Every generates its own distinct cost function, and you can mathematically apply an upper bound (O) to any of them. For example, Insertion Sort's best-case scenario is an already-sorted array, generating a Θ(n) cost function. You can still apply a mathematically valid O(n^2) ceiling to that best-case data.
TAGS: complexity asymptotic_notation case-vs-bound gotcha
---
Q: Which is bigger, `log^2 n` or `log(n^2)`, and what growth class does each belong to?
A: `log^2 n = (log n)^2` is far bigger. 
- `log^2 n` (polylogarithmic): Evaluates as `(log n)^2`, meaning you calculate the log and then square the result.
- `log(n^2)` (logarithmic): Evaluates as the log of n^2, which simplies to `2 log n = Θ(log n)`. 
TAGS: complexity asymptotic_notation growth-classes gotcha
---
Q: As n scales towards infinity, which dominates: `2^n` or `n^2`? Why can't a constant multiplier rescue the loser?
A: 2^n strictly dominates. The limit of n^2 / 2^n -> 0, placing 2^n in a strictly higher exponential class that beats any polynomial. A constant multiplier (c) cannot rescue the polynomial because constants only scales the curve's - it shifts crossover point (n_0) but does not alter the growth class. n^2 multiplied by any fixed c is still o(2^n).
TAGS: complexity asymptotic_notation growth-classes concept
---
Q: `n log n` vs `n + log n`: which is linearithmic and which collapses to linear?
A: The operation between the terms — multiply vs add — decides the class.
- `n log n` (linearithmic): Because it is a product, it scales multiplicatively and sits strictly between linear and quadratic limits - ω(n) and o(n^2).
- `n + log n` (linear): Because it is a sum, log n is a lower-order term to n within the same variable. It drops, leaving Θ(n). 
TAGS: complexity asymptotic_notation simplification gotcha
---
Q: Why can you reduce `O(n^2 + n)` to `O(n^2)`, but not `O(n + m)` to `O(n)`?
A: In n^2 + n, both terms rely on the same variable, meaning n is mathematically guaranteed to act as a lower-order term that washes out at scale. Because n and m are independent variables, m can scale to infinity independently of n, no static constant c can guarantee the inequality n + m <= c * n. Therefore, both terms must be permanently retained. Same reason graph bounds stay O(V + E), two terms.
TAGS: complexity asymptotic_notation simplification gotcha
---
Q: Two blocks each cost O(f) and O(g). When is the total O(f+g)=O(max) vs O(f*g), and how do you systematically identify which to apply?
A: The aggregate complexity is strictly dictated by the control flow architecture.
- Sequential execution (addition → max): Blocks executing one after another sum their bounds, mathematically reducing to the strictly dominant term - O(f+g) = O(max(f,g)).
- Nested iteration (multiplication): A block executing g operations embedded entirely within a loop of f iterations scales multiplicatively - O(f * g). 
TAGS: complexity asymptotic_notation composition concept
---
Q: Distinguish worst-case, average-case, and amortized analysis. What is each quantified over?
A: 
- Worst-case: Evaluates the single most computationally expensive input for an isolated operation.
- Average-case: Evaluates the mathematical expectation over an input distribution, relying heavily on probabilistic assumptions about the data.
- Amortized: Evaluates the per-operation guarantee strictly across a deterministic sequence of interconnected operations, completely devoid of probability. (e.g., A dynamic array append triggers an occasional O(n) resize, but mathematically guarantees an O(1) amortized cost across the sequence). Amortized analysis acts as a separate mathematical axis, never as a fourth data case.
TAGS: complexity asymptotic_notation case-vs-bound concept
---
Q: What is the difference between `little-o` and `Big-O`:regarding tightness?
A: 
- Big-O (<=) permits tightness: n = O(n) holds, meaning a function can equal its bound.
- little-o (<) strictly forbids tightness: f = o(g) asserts that the limit of f/g → 0. The geometric gap between the functions widens without bound, ensuring f is never Θ(g). Every o(g) inherently satisfies O(g), but not vice versa. Use little-o specifically to assert strict algorithmic separation.
TAGS: complexity asymptotic_notation bounds concept
---
Q: When does the base of a logarithm change the complexity class, and when does the base of an exponent? (log2 n vs ln n; 2^n vs 3^n)
A: 
- Logarithmic bases never matter: By the change-of-base identity, log2 n / ln n = 1/ln2 ≈ 1.4427. Because they differ strictly by a constant scalar, they belong to the exact same Θ(ln n) class. 
- Exponential bases dictate the class: 2^n / 3^n = (2/3)^n -> 0. This mathematically proves that 2^n != Θ(3^n). Base differences in exponents fundamentally alter the growth trajectory. Only an additive constant within the exponent is discarded (e.g., 2^(n+1) = 2*2^n = Θ(2^n))
TAGS: complexity asymptotic_notation growth-classes gotcha
---
Q: Which scales worse as n→∞: `n log n` or `n^1.5` (`n√n`)? how do log/polylog factors rank against a polynomial power?
A: `n^1.5` is larger. By dividing both sides by n, the comparison simplifies to `log n` vs `√n`, and `n log n << n√n` (any polynomial power beats any polylog).
TAGS: complexity asymptotic_notation growth-classes gotcha
---