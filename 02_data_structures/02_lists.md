# 02: Lists

A list is an ordered, mutable collection of items.

---

## Creating and Accessing Lists

Create a list by enclosing a comma-separated sequence of items in square brackets `[]`.

Lists use zero-based indexing. You can access any item in the list using its index in square brackets.

```python
# A list of strings
fruits = ["apple", "banana", "cherry"]

# A list with mixed data types
mixed_data = ["apple", 5, True, 3.14]

# Accessing items by index
first_fruit = fruits[0]  # 'apple'
second_item = mixed_data[1] # 5

print("The first fruit is:", first_fruit)

# Negative indexing works just like with strings
last_fruit = fruits[-1] # 'cherry'
print("The last fruit is:", last_fruit)
```

---

## List Slicing

lists can be sliced to access a range of elements.

Syntax: `[start:stop]`, where start is inclusive and stop is exclusive.

```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# Slice from index 1 to 3 (excluding index 3)
some_fruits = fruits[1:3]
print(some_fruits)  # ['banana', 'cherry']

# Omit start or stop
print(fruits[:3])   # First three fruits
print(fruits[2:])   # From index 2 to the end

# Negative indices
print(fruits[-3:-1]) # ['cherry', 'date']
```

---

## Modifying Lists: Mutability

Lists are **mutable**, which means you can change their content after they are created. You can add, remove, or change items in place.

### Changing an Item

Modify an item by assigning a new value to a specific index.

```python
fruits = ["apple", "banana", "cherry"]
print("Original list:", fruits)

# Change the item at index 1
fruits[1] = "blueberry"
print("Modified list:", fruits) # Output: ['apple', 'blueberry', 'cherry']
```

### Adding Items

- `append(item)`: Adds an item to the very end of the list.
- `insert(index, item)`: Inserts an item at a specific index, shifting other items to the right.

```python
fruits = ["apple", "blueberry", "cherry"]
fruits.append("date")      # Adds "date" to the end
print(fruits)

fruits.insert(1, "banana") # Inserts "banana" at index 1
print(fruits)
```

### Removing Items

- `del list[index]`: Removes the item at a specific index.
- `pop(index)`: Removes the item at a specific index and returns it. If no index is provided, it removes and returns the last item.
- `remove(value)`: Removes the first occurrence of a specific value.

```python
fruits = ['apple', 'banana', 'blueberry', 'cherry', 'date']

# Using 'del'
del fruits[2] # Removes 'blueberry'
print(fruits)

# Using 'pop'
last_fruit = fruits.pop() # Removes and returns 'date'
print("Removed fruit:", last_fruit)
print("List after pop:", fruits)

# Using 'remove'
fruits.remove("apple") # Removes the value "apple"
print("Final list:", fruits)
```

---

## Copying Lists

Assigning one list to another variable does not create a new list—it creates a reference to the same list object. Use one of the following techniques to create a shallow copy:

```python
original = [1, 2, 3]

# Shallow copy using slicing
copy1 = original[:]

# Using list() constructor
copy2 = list(original)

# Using copy() method (Python 3.3+)
copy3 = original.copy()
```

Each method creates a new list with the same elements, separate from the original.

---

## List Methods and Functions

| Name           | Type     | Description                                                 |
| -------------- | -------- | ----------------------------------------------------------- |
| `len(list)`    | Function | Returns the number of items in the list.                    |
| `.sort()`      | Method   | Sorts the list in place (modifies the original).            |
| `.reverse()`   | Method   | Reverses the order of items in place.                       |
| `sorted(list)` | Function | Returns a new, sorted list, leaving the original unchanged. |

```python
numbers = [3, 1, 4, 1, 5, 9, 2]
print("Original numbers:", numbers)
print("Length of list:", len(numbers))

# Sort the list in place
numbers.sort()
print("Sorted numbers:", numbers)
```

---

## Membership and Other Operators

Python provides several operators that work with lists:

| Operator | Description                        | Example                   | Result             |
| -------- | ---------------------------------- | ------------------------- | ------------------ |
| `in`     | Returns `True` if value is present | `"a" in "Mars"`           | True               |
| `not in` | Returns `True` if value is absent  | `"z" not in "Mars"`       | True               |
| +        | Concatenates two lists             | fruits + ["fig", "grape"] | New combined list  |
| `*`      | Repeats a list multiple times      | `["hi"] * 3`              | ['hi', 'hi', 'hi'] |

```python
fruits = ["apple", "banana", "cherry"]

print("banana" in fruits)   # True
print("durian" not in fruits) # True

# Concatenation and repetition
new_list = fruits + ["date", "elderberry"]
print(new_list)

repeated = ["hi"] * 3
print(repeated)  # ['hi', 'hi', 'hi']
```

---

## Looping Through a List

The most common way to work with the items in a list is to use a `for` loop.

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I would like to eat a {fruit}.")
```

If you need both the index and the item, use the `enumerate()` built-in function, which provides both on each iteration.

```python
for index, fruit in enumerate(fruits):
    print(f"Item at index {index} is {fruit}.")
```

---

## List Comprehension

A list comprehension provides a concise way to create lists from existing iterables.

```python
# Regular loop
squares = []
for num in range(5):
    squares.append(num ** 2)

# List comprehension version
squares = [num ** 2 for num in range(5)]
print(squares)  # [0, 1, 4, 9, 16]
```

You can also include a condition:

```python
# Get only even numbers
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]
```

---

## Multidimensional Lists

Lists can contain other lists, creating multidimensional or nested structures. These are commonly used for grids, matrices, or tabular data.

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access the element in row 0, column 1
print(matrix[0][1])  # Output: 2

# Iterate over rows and columns
for row in matrix:
    for item in row:
        print(item, end=' ')
```
