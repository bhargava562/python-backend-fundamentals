<div align="center">

# 📘 Day 1 — Python Core Concepts

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OOP](https://img.shields.io/badge/Topic-OOP-blueviolet?style=for-the-badge)
![Day](https://img.shields.io/badge/Day-1-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)

Concepts covered on Day 1 — with real-world analogies, key takeaways,
and references to the corresponding Python files.

</div>

---

## 📑 Table of Contents

| # | Topic | File |
|---|-------|------|
| 1 | [🏗️ Classes & Objects](#1-️-classes--objects) | [`user.py`](./user.py) |
| 2 | [🧬 Inheritance](#2--inheritance) | [`inheritance.py`](./inheritance.py) |
| 3 | [🎨 Decorators](#3--decorators) | [`decorators.py`](./decorators.py) |
| 4 | [🏷️ Type Hints](#4-️-type-hints) | [`type_hints.py`](./type_hints.py) |
| 5 | [🚨 Exception Handling](#5--exception-handling) | [`exceptions.py`](./exceptions.py) |
| 6 | [⚡ Comprehensions](#6--comprehensions) | [`comprehensions.py`](./comprehensions.py) |
| 7 | [🔒 Context Managers](#7--context-managers) | [`context_managers.py`](./context_managers.py) |
| 8 | [🔁 Lambda · map · filter · reduce](#8--lambda--map--filter--reduce) | [`lambda_map_filter.py`](./lambda_map_filter.py) |
| 9 | [📦 *args & **kwargs](#9--args--kwargs) | [`args_kwargs.py`](./args_kwargs.py) |

---

## 1. 🏗️ Classes & Objects

![File](https://img.shields.io/badge/File-user.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-class%20·%20object%20·%20__init__%20·%20__repr__-blueviolet?style=flat-square)

### 📖 What is it?

In the real world, every "thing" has characteristics (what it **is**) and actions (what it **does**).
A **class** is a blueprint that defines both. An **object** is a real instance created from that blueprint.

In Python, a class bundles data (called **attributes**) and actions (called **methods**) into one unit.
The special `__init__` method is the **constructor** — it runs automatically when you create a new object
and sets up its initial data.

### 💡 Real-world Analogy

> Think of a class like a **mobile phone blueprint** drawn by an engineer. The blueprint says every phone
> has a brand, model, and battery level, and can make calls or send texts. An actual Samsung Galaxy or
> iPhone is an **object** — a real phone built from that blueprint. You can have thousands of different
> phones, each with their own data, all made from the same blueprint.

### 🔑 Key Takeaways

| Term | Meaning |
|------|---------|
| `class` | The blueprint / template |
| `object` | A real instance created from the class |
| `self` | Refers to the current object — like saying "my own data" inside a method |
| `__init__` | Constructor — runs automatically when you create an object |
| Class attribute | A variable shared across **all** instances (e.g. `total_users`) |
| Instance attribute | A variable unique to **each** object (e.g. `self.name`) |
| `__repr__` | Controls what `print(obj)` displays — always define for easier debugging |

→ See full implementation in [`user.py`](./user.py)

---

## 2. 🧬 Inheritance

![File](https://img.shields.io/badge/File-inheritance.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-parent%20·%20child%20·%20super()%20·%20polymorphism-blueviolet?style=flat-square)

### 📖 What is it?

Inheritance lets one class **acquire all the features** of another and then extend or change them.
The class that shares its features is the **parent (or base) class**.
The class that inherits is the **child (or derived) class**.

`super()` calls the parent's `__init__` so you don't duplicate setup code.
**Overriding** a method means rewriting it in the child to change its behaviour.
**Polymorphism** means different child objects can respond differently to the same method call.

### 💡 Real-world Analogy

> Think of a **Vehicle** as the parent. Every vehicle has wheels, can start, and can stop.
> A **Car** is a child — it inherits all of that but also adds air conditioning and a trunk.
> A **Truck** is another child — it inherits the same base but adds cargo capacity and a tow hitch.
> You never rewrite "has wheels" for every vehicle — you **inherit** it.

### 🔑 Key Takeaways

| Term | Meaning |
|------|---------|
| `class Child(Parent)` | Child inherits everything from Parent |
| `super().__init__()` | Calls the parent constructor — always do this first in the child |
| Method overriding | Redefine a parent method in the child to change its behaviour |
| Polymorphism | Same method call → different results depending on the object type |
| `isinstance(obj, Parent)` | Returns `True` for both the parent class and any of its children |

→ See full implementation in [`inheritance.py`](./inheritance.py)

---

## 3. 🎨 Decorators

![File](https://img.shields.io/badge/File-decorators.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-@property%20·%20@staticmethod%20·%20@classmethod-blueviolet?style=flat-square)

### 📖 What is it?

Decorators modify the behaviour of methods. Python provides three built-in class decorators,
each serving a distinct purpose.

> **The Ice Cream Analogy:** Think of a decorator like adding toppings to an ice cream cone.
> The base is your plain vanilla cone (the original function). The toppings are chocolate syrup
> or sprinkles (the extra functionality). The result is the same ice cream — just *enhanced*,
> without changing the recipe itself.

### 💡 Real-world Analogies

| Decorator | Analogy | Purpose |
|-----------|---------|---------|
| `@property` | **Hotel minibar** — you can read it (getter) or restock it (setter), but a rule prevents setting a negative quantity | Controlled read/write access to a private attribute |
| `@staticmethod` | **Calculator app** — doesn't need to know whose phone it's on to add 2+2. Pure utility. | Helper function that belongs to the class but needs no instance or class data |
| `@classmethod` | **Factory production line** — accepts raw materials in different forms and produces the same product | Alternative constructors — e.g. `from_dict()`, `from_json()` |

### 🔑 Key Takeaways

| Decorator | Receives | Use When |
|-----------|----------|----------|
| `@property` | `self` (instance) | You want attribute-style access with validation or computed values |
| `@staticmethod` | nothing | The method is a utility and doesn't need `self` or `cls` |
| `@classmethod` | `cls` (the class itself) | You want an alternative way to construct an object |

→ See full implementation in [`decorators.py`](./decorators.py)

---

## 4. 🏷️ Type Hints

![File](https://img.shields.io/badge/File-type__hints.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-Optional%20·%20Union%20·%20list%20·%20dict%20·%20Callable-blueviolet?style=flat-square)

### 📖 What is it?

Type hints are labels you add to tell Python (and other developers) what type of data a function
expects and what it returns. Python does **not** enforce them at runtime, but they make code
self-documenting and allow tools like `mypy` to catch type errors before you even run the program.

### 💡 Real-world Analogy

> Think of a **courier parcel form**. The form has labelled fields: "Recipient Name (text)",
> "Pin Code (6 digits)", "Weight in kg (number)". You're not *forced* to fill them correctly —
> but if you put a name in the Pin Code field, the system will catch the error.
> Type hints are exactly those labels on your code's "form".

### 🔑 Key Takeaways

| Hint | Meaning | Example |
|------|---------|---------|
| `name: str` | Parameter must be a string | `def greet(name: str)` |
| `-> int` | Function returns an integer | `def add(...) -> int` |
| `Optional[str]` | Value is a `str` or `None` | A user lookup that might return nothing |
| `Union[int, str]` | Value can be one of multiple types | A flexible input handler |
| `list[float]` | A list containing floats | A list of prices |
| `dict[str, int]` | A dict with string keys and int values | A name→index catalogue |
| `Callable[[int], int]` | A function that takes an int and returns an int | Passing a function as an argument |

→ See full implementation in [`type_hints.py`](./type_hints.py)

---

## 5. 🚨 Exception Handling

![File](https://img.shields.io/badge/File-exceptions.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-try%20·%20except%20·%20else%20·%20finally%20·%20custom%20exceptions-blueviolet?style=flat-square)

### 📖 What is it?

Exceptions are errors that happen while a program is running. Instead of letting the program crash,
Python lets you **catch** these errors and decide what to do — show a friendly message, retry, or log it.
You can also create **custom exception classes** for more precise, domain-specific error handling.

### 💡 Real-world Analogy

> Think of a **bank ATM**. Multiple things could go wrong: wrong PIN (auth error), insufficient
> balance (funds error), network down (connection error), or card blocked (account error).
> The ATM doesn't freeze — it catches each problem and shows the right message.
> `try/except` is exactly that.
>
> `finally` is like the ATM **always ejecting your card** — whether the transaction succeeded or failed,
> it always returns your card. `finally` always runs, making it perfect for cleanup.

### 🔑 Key Takeaways

| Block | When it runs |
|-------|-------------|
| `try` | The code you want to attempt |
| `except SomeError` | Only if that specific error was raised |
| `except (A, B)` | If either error A or error B was raised |
| `else` | Only if **no** exception occurred |
| `finally` | **Always** — whether or not there was an error. Use for cleanup. |
| Custom exception | Inherit from `Exception` to create named, domain-specific errors |

→ See full implementation in [`exceptions.py`](./exceptions.py)

---

## 6. ⚡ Comprehensions

![File](https://img.shields.io/badge/File-comprehensions.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-list%20·%20dict%20·%20set%20comprehensions-blueviolet?style=flat-square)

### 📖 What is it?

A comprehension is a concise, readable way to build a new list, dictionary, or set from an existing
collection — all in a single line. They are faster than writing a full `for` loop with `.append()`
and are considered **Pythonic** (the idiomatic Python style).

### 💡 Real-world Analogy

> Imagine a **fruit market**. A regular loop is like going through every fruit, picking it up, checking it,
> and manually placing good ones in your basket. A comprehension is like giving an instruction to a machine:
> *"Give me all fruits that are ripe and cost less than ₹50, in uppercase."* — one sentence, same result.

### 🔑 Key Takeaways

| Type | Syntax | Produces |
|------|--------|----------|
| List comprehension | `[expr for item in iterable if condition]` | A new list |
| Dict comprehension | `{key: value for item in iterable if condition}` | A new dictionary |
| Set comprehension | `{expr for item in iterable}` | A new set (unique values only) |

- The `if condition` part is **optional** — leave it out to include all items
- Comprehensions are faster and more readable than equivalent `for` + `append` loops
- Avoid nesting more than two levels — it hurts readability

→ See full implementation in [`comprehensions.py`](./comprehensions.py)

---

## 7. 🔒 Context Managers

![File](https://img.shields.io/badge/File-context__managers.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-with%20·%20__enter__%20·%20__exit__-blueviolet?style=flat-square)

### 📖 What is it?

A context manager wraps code that needs **setup before** and **guaranteed cleanup after** — even if
something crashes in between. The `with` statement is the syntax for using one.

### 💡 Real-world Analogy

> Think of **renting a car**. Before you drive (setup), the rental company checks your licence and
> records the car's condition. After you return it (cleanup), they inspect it and close the booking
> — no matter what happened during the trip. You don't have to remember those steps manually.
> A context manager is that rental system — setup and cleanup are built in.
>
> The most common example is `open()` for files. Without `with`, you'd have to call `file.close()`
> manually. If your code crashes before that line, the file stays open. `with open(...)` **always**
> closes the file — no matter what.

### 🔑 Key Takeaways

| Term | Meaning |
|------|---------|
| `with X as y` | Enters the context, runs the block, then exits cleanly |
| `__enter__` | The setup — runs when the `with` block starts. Returns the resource. |
| `__exit__` | The cleanup — runs when the `with` block ends, even on errors |
| Built-in examples | `open()`, `threading.Lock()`, database connections |
| Custom manager | Create a class with `__enter__` and `__exit__` for your own resources |

→ See full implementation in [`context_managers.py`](./context_managers.py)

---

## 8. 🔁 Lambda · map · filter · reduce

![File](https://img.shields.io/badge/File-lambda__map__filter.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-lambda%20·%20map%20·%20filter%20·%20reduce-blueviolet?style=flat-square)

### 📖 What is it?

A **lambda** is a tiny, nameless function written in one line.
**map** applies a function to every item in a list.
**filter** keeps only items where the function returns `True`.
**reduce** repeatedly combines items into a single accumulated result.

### 💡 Real-world Analogies

| Tool | Analogy |
|------|---------|
| `lambda` | A **sticky note instruction** — "double this number". No name needed, no full page needed. |
| `map` | A **car wash conveyor** — every car goes through the same process and comes out washed. |
| `filter` | A **quality check inspector** on a conveyor belt — only items that pass the test move forward. |
| `reduce` | A **cashier totalling a receipt** — each item's price is added to a running total until all items are included. |

### 🔑 Key Takeaways

| Tool | Input | Output | Use When |
|------|-------|--------|----------|
| `lambda` | arguments | expression result | You need a quick throwaway function |
| `map(fn, list)` | list | transformed list (same size) | Apply the same operation to every item |
| `filter(fn, list)` | list | smaller list (only matches) | Keep items that meet a condition |
| `reduce(fn, list)` | list | single value | Collapse a list into one result (sum, product, etc.) |

- `map` and `filter` return **iterators** — wrap with `list()` to see all results
- `reduce` must be imported from `functools`
- Prefer list comprehensions over `map`/`filter` for readability in most cases — use `map`/`filter` when passing pre-existing functions

→ See full implementation in [`lambda_map_filter.py`](./lambda_map_filter.py)

---

## 9. 📦 \*args & \*\*kwargs

![File](https://img.shields.io/badge/File-args__kwargs.py-lightgrey?style=flat-square&logo=python)
![Concepts](https://img.shields.io/badge/Covers-*args%20·%20**kwargs%20·%20unpacking-blueviolet?style=flat-square)

### 📖 What is it?

`*args` lets a function accept **any number of positional arguments** — they arrive as a tuple.
`**kwargs` lets a function accept **any number of keyword arguments** — they arrive as a dictionary.
Together they make functions extremely flexible when you don't know in advance how many arguments
will be passed.

### 💡 Real-world Analogies

| Syntax | Analogy |
|--------|---------|
| `*args` | A **food delivery bag** — you don't know if someone orders 1 item or 10, the bag stretches to hold whatever is placed inside. |
| `**kwargs` | A **hotel check-in form** with optional fields — "early check-in: yes", "room floor: high", "extra pillow: yes". Named options you can include or skip. |

### 🔑 Key Takeaways

| Syntax | Type inside function | Use When |
|--------|---------------------|----------|
| `*args` | `tuple` | You want to accept any number of positional values |
| `**kwargs` | `dict` | You want to accept any number of named/optional settings |
| Both together | tuple + dict | Building highly flexible functions like order builders or config handlers |
| `**my_dict` (calling) | — | Unpack a dictionary into keyword arguments when calling a function |
| `*my_list` (calling) | — | Unpack a list into positional arguments when calling a function |

- Order in function signature must always be: `regular args` → `*args` → `**kwargs`
- Access `kwargs` values safely with `.get("key", default)` to avoid `KeyError`

→ See full implementation in [`args_kwargs.py`](./args_kwargs.py)

---

<div align="center">

![Concepts](https://img.shields.io/badge/Concepts%20Covered-9-blueviolet?style=for-the-badge)
![Files](https://img.shields.io/badge/Python%20Files-9-3776AB?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Day%201-Complete-brightgreen?style=for-the-badge)

</div>