# Kharazmi

Kharazmi, persian pronunciation of Khwarizmi (al-Khwarizmi, Algorithmi), is an equation parser/calculator module for python.

It's main purpose is to provide an easy method to get equations from user and run them on your own data without using
`eval` and having the freedom of using it on different data types (number, numpy arrays, etc.)

Currently it supports:

- Basic math operations (+-\*/^)
- Numeric Variables (int, float, complex)
- Plugable functions

## Installation

Simply install using pip:

```bash
pip install kharazmi
```

Keep in mind that Kharazmi uses [Python type annotations (PEP 484)](https://www.python.org/dev/peps/pep-0484/), and
[f-Strings (PEP 498)](https://www.python.org/dev/peps/pep-0498/) so you'll need Python 3.6 or higher.

## Usage

### Basic Usage

Kharazmi provides a simple yet powerful API. First of all you have `EquationParser`, the core of the Kharazmi.
It's the main class that you need to worry about. Simply instantiate it and pass your user's input to its `parse` method:

```python
from kharazmi import EquationParser

parser = EquationParser()

user_input = "2*x / (2 - y)"

expression = parser.parse(user_input)
```

All expressions are subclass of `kharazmi.models.BaseNumericalExpression` class. You can work with them as if they were python
variables containing integers, e.g:

```python
expression1 = parser.parse("3*x - y")
expression2 = parser.parse("z")

expression3 = expression1 / expression2
```

You can even build your expressions using normal python code:

```python
x = parser.parse("x")

expression4 = 2*x + 4
```

`BaseNumericalExpression` class provides a `evaluate` method. It allows you to evaluate value of an expression given the values
you provides for variables:

```python
expression5 = parser.parse("2*x + 4")

expression5.evaluate(x=2)
```

Because `Kharazmi` uses python mathematical operators (+-\*/^) under the hood, you can pass any value that supports these
operations and still get the correct result, e.g: you can pass numpy arrays:

```python
import numpy as np

expression6 = parser.parse("2*x + y")

x = np.ones((2,2))
y = np.identity(2)

expression6.evaluate(x=x, y=y)
```

Finally, if you have an expression which you don't know its variables, you can get a list of them using `variables`
property of the expression.

### Using functions

What if you want to create a more complex expressions, like `sin(x)^2 + cos(x)^2`.

Well, first of all, you'll have to tell `kharazmi` the list of your functions:

```python
from math import sin, cos

from kharazmi import register_function

register_function("sin", sin)
register_function("cos", cos)

expression7 = parser.parse("sin(x)^2 + cos(x)^2")
```

You can even have functions with multiple inputs:

```python
register_function("min", min)

expression7 = parser.parse("1 + min(x, y)")
```

If you want to use python's builtin math function, you can use `kharazmi.activate_builtin_math`. Calling this function
will register all builtin functions from `math`, along with `min`, `max`, `round`, and `abs`.

```python
from kharazmi import activate_builtin_math

activate_builtin_math()

expression8 = parser.parse("log2(8)")
```

### Using as a module

You can run `kharazmi` as a module using `python -m kharazmi`, this will run a REPL like program that lets you enter
expressions, see how you can do the same thing in code, in other words how `kharazmi` is understanding your input, and
evaluate it.

It supports all math function either.

It's mostly for debugging and testing purposes, but it's there if you want to understand how `kharazmi` is working,
I suggest start from there.
