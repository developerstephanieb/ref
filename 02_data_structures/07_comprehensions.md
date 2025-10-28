# 07: Comprehensions

A **comprehension** is a compact way to create a new data structure by iterating over an existing one. They are a hallmark of idiomatic Python code because they are often more readable and efficient than using a standard for loop.

---

## List Comprehensions

A **list comprehension** provides a concise syntax for creating a new list based on the values of an existing iterable.

Standard `for` Loop:

```python
# Create a list of squares from the numbers 0 through 9.
squares = []
for x in range(10):
    squares.append(x ** 2)

print(squares)
```

List comprehension equivalent:

The basic syntax is `[expression for item in iterable]`.

```python
# Create the same list using a comprehension.
squares = [x ** 2 for x in range(10)]

print(squares)
```

### Adding a condition

List comprehensions can also include an optional `if` clause to filter items from the source iterable. The syntax is `[expression for item in iterable if condition]`.

Standard for loop with a condition:

```python
# Create a list of only the even squares.
even_squares = []
for x in range(10):
    if x % 2 == 0:
        even_squares.append(x ** 2)

print(even_squares)
```

List comprehension with a condition:

```python
# Create the same list using a comprehension with a filter.
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]

print(even_squares)
```

---

## Set Comprehensions

The syntax for a **set comprehension** is nearly identical to a list comprehension, but it uses curly braces `{}` instead of square brackets `[]`. The result is a new set, which means any duplicate values produced by the expression will be automatically removed.

---