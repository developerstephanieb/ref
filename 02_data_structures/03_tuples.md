# 03: Tuples

A **tuple** is an ordered, immutable collection of items. It is very similar to a list, but with one critical difference: once a tuple is created, its contents cannot be changed.

---

## Creating and Accessing Tuples

Create a tuple by enclosing a comma-separated sequence of items in parentheses `()`.

Tuples are zero-indexed, and you can access items using square brackets `[]`.

```python
# A tuple of numbers representing coordinates.
point = (10, 20, 30)

# A tuple with mixed data types.
record = ("Alice", 30, "admin")

# Accessing items by index.
x_coordinate = point[0]
user_name = record[0]

print("X Coordinate:", x_coordinate) # Output: 10
print("User:", user_name)           # Output: Alice
```

### Single Item Tuple

Creating a tuple with a single item has a special syntax: you must include a trailing comma. Without the comma, Python will not recognize it as a tuple.

```python
# The comma is required for single-item tuples.
single_item_tuple = (99,)
not_a_tuple = (99)

print("Type of single_item_tuple:", type(single_item_tuple)) # Output: <class 'tuple'>
print("Type of not_a_tuple:", type(not_a_tuple))       # Output: <class 'int'>
```

---

## Immutability

The defining feature of a tuple is that it cannot be changed after creation. You cannot reassign an item, add new items, or remove items. Attempting to do so will result in a `TypeError`.

```python
point = (10, 20, 30)

# This code will fail because tuples are immutable.
# point[0] = 15 # TypeError: 'tuple' object does not support item assignment
```

---

## Tuple Unpacking

**Unpacking** allows you to assign the items of a tuple to multiple variables in a single statement.

```python
# Define a tuple representing a user record.
user_record = ("Alice", 30, "admin")

# Unpack the tuple into individual variables.
name, age, role = user_record

# Now you can use the variables directly.
print("Name:", name)
print("Age:", age)
print("Role:", role)
```

---

## Tuple Methods

Although tuples are immutable, they support a few built-in methods

| Method          | Description                                             |
| --------------- | ------------------------------------------------------- |
| `.count(value)` | Returns the number of times value appears in the tuple. |
| `.index(value)` | Returns the index of the first occurrence of value.     |

```python
data = (1, 2, 2, 3, 4, 2)

print(data.count(2))  # Output: 3
print(data.index(3))  # Output: 3
```

---

## Nested Tuples

Tuples can contain other tuples (or lists)

```python
# A nested tuple representing students and their grades.
students = (
    ("Alice", 90),
    ("Bob", 85),
    ("Charlie", 92)
)

for student in students:
    name, grade = student
    print(f"{name} scored {grade}")
```

---

## Tuple vs List

Use a list when:

- You have a collection of items that needs to change over time (add, remove, or modify items).

T- he items in the collection are homogeneous (all of the same type).

Use a tuple when:

- You have a collection of items that should not change for the lifetime of the program.

- You want to represent a single, fixed record of heterogeneous data (e.g., a point with x, y, z coordinates).
