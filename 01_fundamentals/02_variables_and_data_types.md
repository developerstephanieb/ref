# 02: Variables and Data Types

This guide introduces variables and the fundamental types of data they can hold.

---

## Variables

A **variable** is a named reference to a value stored in memory. It serves as a label for a piece of data.

Create a variable by choosing a name and assigning a value to it using the **assignment operator** (`=`).

```python
planet = "Earth"
continents = 7
```

---

## Dynamic Typing

Python is a **dynamically typed** language. This means variable types are determined when the program runs (**runtime**).

Variables can be **reassigned** to a different value and type.

```python
population = 8000000000
population = "Eight billion"
```

---

## Naming Variables

Python variables are named according to specific rules and conventions.

### Rules

In Python, **syntax** refers to the set of rules that define how code must be written. Variable names must follow these rules to be valid.

- A variable name must start with a letter (`a-z`, `A-Z`) or an underscore (`_`).
- Cannot start with a number.
- Can only contain letters, numbers, and underscores.
- Names are case-sensitive (`sea`, `Sea`, and `SEA` are three different variables).

### Conventions (`PEP 8`)

Beyond the rules, the [PEP 8](https://peps.python.org/pep-0008/) style guide defines standard naming conventions.

- Use `snake_case` (all lowercase words separated by underscores).
- Choose short, descriptive names that clearly communicate the purpose.
- Good Names: `first_name`, `user_input`, `mph`   
- Bad Names: `FirstName`, `1st_name`, `u`, `milesperhour`

### Constants

A **constant** is a variable whose value is not meant to change. Python doesn't enforce this, but the convention is to name constants in `UPPERCASE_WITH_UNDERSCORES`.

```python
GRAVITY = 9.81
EARTH_RADIUS_KM = 6371
```

### Keywords

**Keywords** are reserved words that are part of Python’s syntax. They cannot be used as variable names.

```python
if, else, elif, while, for, def, return, class, import, True, False, None
```

---

## Data Types

A **data type** is a classification that specifies which kind of value a variable can hold and what operations can be performed on that value.

### Strings (`str`)

A **string** is a sequence of characters used to represent text. Create strings using single (`'`) or double (`"`) quotes.  A string can contain one type of quotation mark when enclosed by the other. 

```python
country = "Brazil"
climate_fact = 'The Amazon is often called the "lungs of the Earth" because of its vast oxygen production.'
```

### Integers (`int`)

**Integers** are whole numbers. For large numbers, underscores can be used as visual separators to improve readability. Python ignores the underscores when storing the values.

```python
rainforest_types = 2
trees_in_amazon = 390_000_000_000
```

### Floats (`float`)

A **float**, or floating-point number, is a number with a decimal component.

```python
core_temperature = 5_700.5
surface_water_coverage = 70.8 
```

### Booleans (`bool`)

A **boolean** represents either `True` or `False`.

```python
is_habitable = True
has_rings = False
```

---

## Methods

A **method** is an action that Python can perform on a piece of data. It is called using **dot notation**, which means writing the variable’s name, followed by a dot (`.`), the method’s name, and parentheses `()`. Every method is followed by a set of parentheses, because methods often need additional information to do their work. That information is provided inside the parentheses.

### The `.title()` Method

The `.title()` method capitalizes the first letter of each word in a string.

Syntax: `string.title()`

```python
landmark = "mount everest, nepal"

print(landmark.title())
```

The program will print `Mount Everest, Nepal` to the terminal.

---

## Built-in Functions

A **built-in function** is a tool provided as part of the language that can be used directly. It is called by writing the function’s name, followed by parentheses `()` containing the data it should work on.

### The `type()` Function

To determine the data type of a variable, use the built-in `type()` function. 

Syntax: `type(object)`

```python
spacecraft = "Voyager 1"

print(type(spacecraft))
```

The program will print `<class 'str'>` to the terminal.

---

## Runtime Errors and Tracebacks

An error that occurs while a program is running is called a **runtime error**. When this happens, Python stops and displays a **traceback**, a message that explains where and why the error happened.

### `NameError`

This runtime error happens when a variable is used before it has been defined, often due to a typo.

```python
message = "Welcome to Earth"
print(mesage)
```

Because `message` was misspelled as `mesage`, Python doesn't recognize the variable and raises an error. 

```bash
Traceback (most recent call last):
  File "/path/to/your/file.py", line 2, in <module>
    print(mesage)
NameError: name 'mesage' is not defined
```

### How to Read a Traceback

The traceback message helps identify and fix errors.

- **File and Line Number**: `File "/path/to/your/file.py", line 2` indicates where the error occurred.
- **The Failing Code**: `print(mesage)` displays the line that caused the crash.
- **The Error Type**: `NameError` specifies the error type.
- **The Error Message**: `name 'mesage' is not defined` details the cause of the error.
