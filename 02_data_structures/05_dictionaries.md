# 05: Dictionaries

**mapping type**

A **dictionary** is an unordered, mutable collection that stores data not as a sequence, but as a set of key-value pairs.

Each **key** in a dictionary is unique and is used to access its corresponding **value**. This model is extremely useful for storing data that has a clear label, like a user's profile or a set of configuration settings.

---

## Creating Dictionaries

Create a dictionary by enclosing a comma-separated list of `key: value` pairs in curly braces `{}`.

- **Keys** must be of an immutable type (strings and numbers are most common).
- **Values** can be of any data type.

```python
# A dictionary representing a user's profile.
user_profile = {
    "username": "ada_lovelace",
    "email": "ada@example.com",
    "age": 36,
    "is_active": True
}

print(user_profile)

# You can also create an empty dictionary.
empty_dict = {}
```

---

## Accessing, Adding, and Modifying Items

Instead of using an index, you access values in a dictionary using their corresponding key in square brackets `[]`.

### Accessing a Value

```python
user_profile = {"username": "ada_lovelace", "age": 36}

# Access the value associated with the 'username' key.
name = user_profile["username"]
print("Username:", name)
```

If you try to access a key that does not exist, Python will raise a `KeyError`.

### Adding or Modifying a Key-Value Pair

You can add a new key-value pair or modify an existing one using the same square bracket assignment syntax.

```python
user_profile = {"username": "ada_lovelace", "age": 36}

# Add a new key-value pair.
user_profile["role"] = "admin"
print("After adding role:", user_profile)

# Modify the value of an existing key.
user_profile["age"] = 37
print("After modifying age:", user_profile)
```

---

## Removing Key-Value Pairs

You can remove items from a dictionary using the `del` statement or the `.pop()` method.

`del dict[key]`: Removes the key-value pair with the specified key.

`.pop(key)`: Removes the key-value pair and returns the value.

```python
user_profile = {"username": "ada_lovelace", "age": 37, "role": "admin"}

# Using 'del' to remove the 'role' key.
del user_profile["role"]
print("After del:", user_profile)

# Using 'pop' to remove the 'age' key and get its value.
removed_age = user_profile.pop("age")
print("Removed age:", removed_age)
print("Final dictionary:", user_profile)
```

---

## Looping Through a Dictionary

There are several ways to loop through a dictionary, depending on whether you need the keys, the values, or both.

### Looping Through Keys

By default, iterating over a dictionary gives you its keys.

```python
user_profile = {"username": "ada_lovelace", "age": 37}

for key in user_profile:
    print(f"Key: {key}, Value: {user_profile[key]}")
```

### Looping Through Values

Use the `.values()` method to iterate directly over the values.

```python
for value in user_profile.values():
    print("Value:", value)
```

### Looping Through Keys and Values

The most common and efficient way to loop is using the `.items()` method, which gives you a tuple of `(key, value)` for each item on every iteration.

```python
for key, value in user_profile.items():
    print(f"The key is '{key}' and the value is '{value}'.")
```

---

## Tuples as Dictionary Keys

Since tuples are hashable (if all their elements are immutable), they can be used as keys in dictionaries

```python
# Coordinates as keys
locations = {
    (40.7128, -74.0060): "New York",
    (34.0522, -118.2437): "Los Angeles"
}

print(locations[(40.7128, -74.0060)])  # Output: New York
```

---

## Dictionary Methods

| Method                   | Description                                                        |
| ------------------------ | ------------------------------------------------------------------ |
| dict.get(key[, default]) | Returns the value for key if it exists, otherwise returns default. |
| dict.keys()              | Returns a view of all keys in the dictionary.                      |
| dict.values()            | Returns a view of all values in the dictionary.                    |
| dict.items()             | Returns a view of key-value pairs as tuples.                       |
| dict.update(other_dict)  | Adds key-value pairs from other_dict, overwriting duplicates.      |
| dict.clear()             | Removes all items from the dictionary.                             |

```python
profile = {"username": "ada_lovelace", "email": "ada@example.com"}

# Get with default
print(profile.get("age", "Not specified"))  # Output: Not specified

# Update
profile.update({"age": 36, "is_active": True})
print(profile)

# Clear all items
profile.clear()
print(profile)  # Output: {}
```

---

## in Keyword for Membership Testing

You can check if a key exists in a dictionary using the in keyword.

```python
user_profile = {"username": "ada_lovelace", "age": 37}

if "age" in user_profile:
    print("Age is available.")
```

---

## Nesting Dictionaries

Dictionaries can contain other dictionaries, which is common for representing structured data.

```python
users = {
    "alice": {"email": "alice@example.com", "active": True},
    "bob": {"email": "bob@example.com", "active": False}
}

print(users["alice"]["email"])  # Output: alice@example.com
```