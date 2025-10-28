# 01: Strings

A string is a data type that represents text as an ordered sequence of characters. It is considered a **sequence data type**, meaning its elements are arranged in a specific order and can be accessed by index. A string also functions as a **data structure**, a defined way of organizing and storing data.

---

## Accessing Characters by Index

Individual characters in a string can be accessed by their **index**. An index is an integer representing the character’s position in the sequence. Python uses zero-based indexing, so the first character is at index `0`.

Use square brackets `[]` to access a character at a specific index.

```python
message = "Hello, World!"

# Access the first character
first_char = message[0]
print("First character:", first_char) # Output: H

# Access the eighth character
eighth_char = message[7]
print("Eighth character:", eighth_char) # Output: W
```

Negative indices can be used to access characters from the end of a string. The index `-1` refers to the last character, `-2` to the second-to-last, and so on.

```python
# Access the last character
last_char = message[-1]
print("Last character:", last_char) # Output: !
```

---

## Slicing Strings to Get Substrings

**Slicing** is the process of creating a substring (a portion of a string).

Syntax: `[start:stop]`
- `start`: The index where the slice begins (inclusive). If omitted, it defaults to the beginning of the string.
- `stop`: The index where the slice ends (exclusive). If omitted, it defaults to the end of the string.

```python
message = "Hello, World!"

# Get the substring from index 0 up to (but not including) index 5
greeting = message[0:5]
print(greeting) # Output: Hello

# Omitting the start index defaults to 0
also_greeting = message[:5]
print(also_greeting) # Output: Hello

# Omitting the stop index defaults to the end
subject = message[7:]
print(subject) # Output: World!
```

---

## Immutability

Strings in Python is that are **immutable**, meaning its contents cannot be changed after creation. Any operation or method that appears to modify a string actually creates and returns a new string.

```python
name = "sam"

# The .capitalize() method does not change the original 'name' variable.
# It returns a new string, which we can store.
capitalized_name = name.capitalize()

print("Original name:", name)             # Output: sam
print("Capitalized name:", capitalized_name) # Output: Sam
```

Attempting to change a character by its index will result in a `TypeError`.

```python
# This code will fail
name = "sam"
name[0] = "P" # TypeError: 'str' object does not support item assignment
```

---

## Escape Sequences

**Escape sequences** allow special characters to be included in strings. Each begins with a backslash (`\`).

| Sequence | Meaning           |
| :------: | ----------------- |
|   `\n`   | Newline           |
|   `\t`   | Horizontal Tab    |
|   `\\`   | Literal Backslash |
|   `\'`   | Single Quote      |
|   `\"`   | Double Quote      |

---

## Raw Strings

Prefixing a string with `r` creates a **raw string**, which treats backslashes `\` as literal characters.

```python
# Using a raw string for a file path is much cleaner
raw_path = r"C:\Users\Default\Documents\new_folder"
print(raw_path)
```

---

## String Operations

Use operators for common string operations like concatenation, repetition, and membership testing.

| Operator | Name          | Example                              |
| -------- | ------------- | ------------------------------------ |
| `+`      | Concatenation | `'a' + 'b'` results in `'ab'`        |
| `*`      | Repetition    | `'a' * 3` results in `'aaa'`         |
| `in`     | Membership    | `'a' in 'cat'` results in `True`     |
| `not in` | Membership    | `'b' not in 'cat'` results in `True` |

---

## Whitespace

whitespace: any nonprinting characters, such as spaces, tabs, and end-of-line symbols.

### Adding Whitespace to Strings

| Sequence | Meaning        |
| :------: | -------------- |
|   `\n`   | Newline        |
|   `\t`   | Horizontal Tab |

### Striping Whitespace from Strings

When the stripping method acts on the variable, this extra space is removed temporarily. 
To remove the whitespace from the string permanently, you have to associate the stripped value with the variable name

```python
favorite_language = ' Python '
print(favorite_language.strip()) # temporarily remove
favorite_language = favorite_language.strip() # permanent removal

print(favorite_language)
```

Output
```bash
Python
```

---

### Removing Prefixes & Suffixes

#### removeprefix()

When working with strings, another common task is to remove a prefix

```python
url = 'https://python.org'
print(url.removeprefix('https://'))
```

Output
```bash
python.org
```

#### removesuffix()

```python
file_name = 'python_notes.txt'
print(file_name.removesuffix('.txt'))
```

Output
```bash
python_notes
```

---

## String Methods

The following table lists commonly used string methods in Python. 

| Method                  | Description                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| `str.lower()`           | Returns a copy of the string with all characters converted to lowercase.     |
| `str.upper()`           | Returns a copy of the string with all characters converted to uppercase.     |
| `str.capitalize()`      | Returns a copy with the first character capitalized and the rest lowercased. |
| `str.title()`           | Returns a copy with the first character of each word capitalized.            |
| `str.strip()`           | Removes leading and trailing whitespace (or specified characters).           |
| `str.lstrip()`          | Removes leading whitespace (or specified characters).                        |
| `str.rstrip()`          | Removes trailing whitespace (or specified characters).                       |
| `str.replace(old, new)` | Replaces all occurrences of `old` with `new`.                                |
| `str.find(sub)`         | Returns the lowest index where substring `sub` is found, or `-1` if not.     |
| `str.count(sub)`        | Returns the number of occurrences of substring `sub`.                        |
| `str.startswith(x)`     | Returns `True` if the string starts with substring `x`.                      |
| `str.endswith(x)`       | Returns `True` if the string ends with substring `x`.                        |
| `str.split(sep)`        | Splits the string into a list using `sep` as the delimiter.                  |
| `str.join(iterable)`    | Joins elements of an iterable into a single string, separated by the string. |
| `str.isalpha()`         | Returns `True` if all characters are alphabetic.                             |
| `str.isdigit()`         | Returns `True` if all characters are digits.                                 |
| `str.isalnum()`         | Returns `True` if all characters are alphanumeric.                           |
| `str.isspace()`         | Returns `True` if all characters are whitespace.                             |
| `str.swapcase()`        | Returns a copy with uppercase characters lowered and vice versa.             |

---

## String Formatting with F-Strings

An **f-string** (formatted string literal) is a way to embed expressions inside string literals. Create an f-string by prefixing the string with the letter `f`. Enclose any variable or expression to embed in curly braces `{}`.

```python
name = "Ada"
age = 36

# Using an f-string to embed variables directly into the string.
message = f"Hello, my name is {name} and I am {age} years old."
print(message)

# You can also put expressions inside the braces.
print(f"In ten years, she will be {age + 10} years old.")
```
