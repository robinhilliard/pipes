## Elixir–Style Pipes for Python

In the Elixir programming language the `|>` pipe operator allows you to chain together
multiple function calls so that this:

```$elixir 
c(b(a(1, 2), 3, 4))
```

can be written more readably as:

```$elixir
1 |> a(2) |> b(3, 4) |> c()
```

All the pipe operator does is pass its left operand as the first argument of the right operand,
so that `a |> b(...)` becomes `b(a, ...)`.

Various pipe implementations in Python to date allow a list of functions to be applied
to an initial value, but do not support the partial, missing first argument syntax of Elixir.

This library provides a function decorator that causes Python `>>` right shift operators within the
function to act exactly like Elixir pipes:

```$python
from pipes import pipes

def add(a, b):
    return a + b
    
def times(a, b):
    return a * b
    
@pipes
def calc()
    print 1 >> add(2) >> times(3)  # prints 9
``` 

Functions can have any number of arguments:

```$python
def add3(a, b, c):
    return a + b + c
    
@pipes
def calc()
    print 1 >> add3(2, 3)  # prints 6
```

There should be a small amount of processing overhead the first time the function is called,
otherwise there should be no difference to the conventionally nested call code.

This is initial alpha code. It has been tested on Python 2.7.14 using simple functions. It has
not been tested using bound methods or Python 3. Source line attributes are preserved so
debuggers should be able to follow the code as it executes. Pull requests and bug reports gratefully accepted.

Robin Hilliard