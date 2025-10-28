# 06: Mutability and Copying

several data structures and learned that some are mutable (can be changed) and others are immutable (cannot be changed). Understanding mutability is essential for writing reliable Python code. It affects how variables behave, how data is passed into functions, and whether changes to one variable might unexpectedly affect another.

---

## Understanding Mutability

A variable doesn't hold the data itself, but rather a reference—like a memory address—to where the data is stored.

- Immutable Types: `str`, `int`, `float`, `bool`, `tuple`
When an operation appears to "change" an immutable object, Python actually creates a new object in memory and makes the variable point to it.

- Mutable Types: `list`, `set`, `dict`
When you modify a mutable object (e.g., using `.append()` or `my_list[0] = ...)`, you are changing the original object directly in its memory location.

---

## Mutability's Effect on Functions

The most common place where mutability causes unexpected behavior is when passing arguments to functions.

- When you pass an immutable object (like a number) to a function, you don't have to worry about the function changing your original variable.

- When you pass a mutable object (like a list) to a function, the function receives a reference to the exact same object. Any modifications the function makes will affect the original list outside the function.

```python
# Define a function that modifies a list.
def add_item_to_list(items_list):
    print("Inside function, before append:", items_list)
    items_list.append("new item")
    print("Inside function, after append:", items_list)

# Create a list.
my_shopping_list = ["apples", "bananas"]
print("Outside function, before call:", my_shopping_list)

# Pass the mutable list to the function.
add_item_to_list(my_shopping_list)

# The original list has been changed!
print("Outside function, after call:", my_shopping_list)
```

---

## Assignment, Shallow Copies, and Deep Copies

When working with mutable data, it's critical to understand the difference between creating a copy and simply assigning a new variable to the same object.

### Assignment (`=`)

Simple assignment does not create a copy. It creates a new variable that points to the exact same object in memory.

```python
# Create a list.
list_a = [1, 2, 3]

# This does NOT create a new list.
# Both 'list_a' and 'list_b' now point to the same object.
list_b = list_a

# Modifying list_b will also affect list_a.
list_b.append(4)

print("List A:", list_a) # Output: [1, 2, 3, 4]
print("List B:", list_b) # Output: [1, 2, 3, 4]
```

### Shallow Copy

A **shallow copy** creates a new object but then inserts references to the objects found in the original. For a simple list of numbers, this works like a true copy. However, if the list contains other mutable objects (like other lists), the shallow copy will only copy the references to those nested objects.

Create a shallow copy using the `.copy()` method or by slicing the entire list (`[:]`).

```python
# Create a nested list (a list containing another list).
list_a = [1, 2, [10, 20]]

# Create a shallow copy.
list_b = list_a.copy()

# Modify the nested list inside list_b.
list_b[2].append(30)

# The change is reflected in BOTH lists because they share a reference
# to the same inner list object.
print("List A:", list_a) # Output: [1, 2, [10, 20, 30]]
print("List B:", list_b) # Output: [1, 2, [10, 20, 30]]
```

### Deep Copy

A **deep copy** creates a completely independent copy of the original object and all the objects it contains, recursively. This is the safest way to ensure that changes to a copy will never affect the original, but it is also the most memory-intensive.

To perform a deep copy, you must import the `copy` module.

```python
import copy

# Create a nested list.
list_a = [1, 2, [10, 20]]

# Create a deep copy.
list_b = copy.deepcopy(list_a)

# Modify the nested list inside list_b.
list_b[2].append(30)

# The original list_a remains unchanged.
print("List A:", list_a) # Output: [1, 2, [10, 20]]
print("List B:", list_b) # Output: [1, 2, [10, 20, 30]]
```

---

## Object Identity

You can check whether two variables point to the same object in memory using the is operator or the built-in id() function.

```python
a = [1, 2, 3]
b = a
c = a.copy()

print(a is b)  # True: same object
print(a is c)  # False: different objects
print(id(a), id(b), id(c))  # See memory addresses
```

