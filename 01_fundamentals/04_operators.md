# 04: Operators

**Operators** are special symbols or keywords used to perform operations on values, such as math, comparisons, or logic.

---

## Arithmetic Operators

Arithmetic operators are used to perform mathematical calculations with numbers.

| Operator | Name           | Example  |   Result   |
| :------: | -------------- | :------: | :--------: |
|   `+`    | Addition       | `5 + 3`  |    `8`     |
|   `-`    | Subtraction    | `5 - 3`  |    `2`     |
|   `*`    | Multiplication | `5 * 3`  |    `15`    |
|   `/`    | Division       | `5 / 3`  | `1.666...` |
|   `//`   | Floor Division | `5 // 3` |    `1`     |
|   `%`    | Modulus        | `5 % 3`  |    `2`     |
|   `**`   | Exponentiation | `5 ** 3` |   `125`    |

*Note*: Division (`/`) always results in a float, even if the numbers divide evenly. In other operations, mixing an integer with a float also produces a float.

---

## String Concatenation

The `+` operator has a different meaning when used with strings. It joins them together in an operation called **concatenation**.

```python
mission = "Apollo"
number = "11"
separator = " "

# Join the strings together
mission_name = mission + separator + number
print(mission_name)  # Output: Apollo 11
```

### `TypeError`

The `+` operator cannot be used to combine two different data types. This will cause **type error**, a runtime error that occurs when an operation is performed on a value of the wrong type. When this happens, the interpreter stops and displays a `TypeError`.

```python
# This code will fail
launch_year = 1969
message = "Launch year: " + launch_year
```

Error: `TypeError: can only concatenate str (not "int") to str`

---

## Assignment Operators

Assignment operators are used to assign values to variables.

| Operator | Example  | Equivalent to |
| :------: | :------: | :-----------: |
|   `+=`   | `x += 3` |  `x = x + 3`  |
|   `-=`   | `x -= 3` |  `x = x - 3`  |
|   `*=`   | `x *= 3` |  `x = x * 3`  |
|   `/=`   | `x /= 3` |  `x = x / 3`  |

---

## Comparison Operators

Comparison operators are used to compare two values. The result of a comparison is always a boolean value: `True` or `False`.

| Operator | Name                     | Example  |
| :------: | ------------------------ | :------: |
|   `==`   | Equal to                 | `x == y` |
|   `!=`   | Not equal to             | `x != y` |
|   `>`    | Greater than             | `x > y`  |
|   `<`    | Less than                | `x < y`  |
|   `>=`   | Greater than or equal to | `x >= y` |
|   `<=`   | Less than or equal to    | `x <= y` |

---

## Logical Operators

Logical operators are used to combine boolean values.

| Operator | Description                                     | Example            |
| :------: | ----------------------------------------------- | ------------------ |
|  `and`   | Return `True` if both statements are true       | `x > 5 and y < 10` |
|   `or`   | Returns `True` if one of the statements is true | `x > 5 or y > 10`  |
|  `not`   | Returns `False` if the result is true           | `not(x > 5)`       |

---

## Identity Operators

Identity operators check whether two variables refer to the exact same object in memory, not just whether their values are equal.


| Operator | Description                                        | Example      |
| :------: | -------------------------------------------------- | ------------ |
|   `is`   | Returns `True` if both refer to the same object    | `x is y`     |
| `is not` | Returns `True` if both  refer to different objects | `x is not y` |

---

## Membership Operators

Membership operators test whether a value exists within a sequence.

| Operator | Description                        | Example             |
| :------: | ---------------------------------- | ------------------- |
|   `in`   | Returns `True` if value is present | `"a" in "Mars"`     |
| `not in` | Returns `True` if value is absent  | `"z" not in "Mars"` |

---

## Bitwise Operators

Bitwise operators perform operations on the binary representations of integers.

| Operator | Name                | Example  | Result |
| :------: | ------------------- | :------: | :----: |
|   `&`    | Bitwise AND         | `5 & 3`  |  `1`   |
|   `\|`   | Bitwise OR          | `5 \| 3` |  `7`   |
|   `~`    | Bitwise NOT         |   `~5`   |  `-6`  |
|   `^`    | Bitwise XOR         | `5 ^ 3`  |  `6`   |
|   `>>`   | Bitwise right shift | `5 >> 1` |  `2`   |
|   `<<`   | Bitwise left shift  | `5 << 1` |  `10`  |
