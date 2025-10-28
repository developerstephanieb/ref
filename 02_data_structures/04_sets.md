# 04: Sets

A **set** is an unordered, mutable collection of unique items.

Their main characteristics are:

- Uniqueness: A set cannot contain duplicate items.

- Unordered: Items in a set do not have a defined order. You cannot access items using an index.

- Mutability: You can add and remove items from a set.

Sets are highly optimized for membership testing (`in`) and for performing mathematical set operations.

---

## Creating Sets

Create a set by enclosing a comma-separated sequence of items in curly braces `{}`. You can also use the `set()` function to create a set from another iterable, like a list.

```python
# Create a set using curly braces. Note the duplicate 'apple' is removed.
fruits = {"apple", "banana", "cherry", "apple"}
print(fruits) # Output might be {'cherry', 'apple', 'banana'} - order is not guaranteed.

# Create a set from a list to remove duplicates.
numbers_list = [1, 2, 2, 3, 4, 3]
unique_numbers = set(numbers_list)
print(unique_numbers) # Output: {1, 2, 3, 4}
```

To create an empty set, you must use the `set()` function. Using empty curly braces `{}` will create an empty dictionary.

```python
# Correct way to create an empty set.
empty_s = set()

# This creates an empty dictionary, not a set.
empty_d = {}
```

---

## Adding and Removing Items

Since sets are mutable, you can modify them after creation.

- `.add(item)`: Adds a single item to the set. If the item is already present, the set remains unchanged.

- `.update(other_set)`: Adds all items from another set (or any other iterable).

- `.remove(item)`: Removes a specific item. Raises a KeyError if the item is not found.

- `.discard(item)`: Removes a specific item, but does not raise an error if the item is not found.

- `.pop()`: Removes and returns an arbitrary item from the set.

- `.clear()`: Removes all items from the set.

```python
permissions = {"read", "write"}
print("Initial permissions:", permissions)

# Add a new permission.
permissions.add("execute")
print("After add:", permissions)

# Remove a permission.
permissions.remove("write")
print("After remove:", permissions)

# Discard a permission that doesn't exist (no error).
permissions.discard("admin")
print("After discard:", permissions)
```

---

## Set Operations

The true power of sets comes from their ability to perform mathematical set operations efficiently. These are often used to compare two collections of data.

Given two sets, `set_a` and `set_b`:

| Method                              | Operator        | Description                                                              |
| ----------------------------------- | --------------- | ------------------------------------------------------------------------ |
| `set_a.union(set_b)`                | `set_a`         | `set_b`                                                                  |
| `set_a.intersection(set_b)`         | `set_a & set_b` | Returns a new set with only the items present in both sets.              |
| `set_a.difference(set_b)`           | `set_a - set_b` | Returns a new set with items in `set_a` but not in `set_b`.              |
| `set_a.symmetric_difference(set_b)` | `set_a ^ set_b` | Returns a new set with items in either `set_a` or `set_b`, but not both. |

```python
local_permissions = {"read", "write", "comment"}
admin_permissions = {"read", "write", "execute", "delete"}

# Union: All unique permissions combined.
all_perms = local_permissions.union(admin_permissions)
print("Union:", all_perms)

# Intersection: Permissions they have in common.
common_perms = local_permissions.intersection(admin_permissions)
print("Intersection:", common_perms)

# Difference: Permissions admins have that local users don't.
unique_to_admin = admin_permissions.difference(local_permissions)
print("Difference:", unique_to_admin)
```

---

## Membership Testing

Sets are optimized for fast membership checks using the `in` keyword.

```python
features = {"login", "signup", "logout"}

print("login" in features)   # True
print("profile" in features) # False
```

---

## Set Comparison and Subset/Superset Relationships

Sets support comparisons to test subset and superset relationships.

| Expression              | Description                                  |
| ----------------------- | -------------------------------------------- |
| set_a == set_b          | True if both sets contain the same elements. |
| set_a.issubset(set_b)   | True if all elements of set_a are in set_b.  |
| set_a.issuperset(set_b) | True if all elements of set_b are in set_a.  |
| set_a.isdisjoint(set_b) | True if the sets share no elements.          |

```python
core = {"read", "write"}
extended = {"read", "write", "execute"}

print(core.issubset(extended))   # True
print(extended.issuperset(core)) # True
print(core.isdisjoint({"delete"})) # True
```

---

## Frozen Sets

If you need an immutable set, use a `frozenset`. It behaves like a regular set but cannot be modified.

```python
roles = frozenset(["user", "admin"])

# roles.add("guest") # Raises AttributeError
print("admin" in roles) # True
```
