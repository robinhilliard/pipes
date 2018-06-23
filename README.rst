In the Elixir programming language the ``|>`` pipe operator allows you
to chain together multiple function calls so that this::

  c(b(a(1, 2), 3, 4))

can be written more readably as::

  1 |> a(2) |> b(3, 4) |> c()

All the pipe operator does is pass its left operand as the first argument of
the right operand, so that ``a |> b(...)`` becomes ``b(a, ...)``.

Various pipe implementations in Python to date allow a list of functions to be
applied to an initial value, but do not support the partial, missing first
argument syntax of Elixir.

This library provides a function decorator that causes Python ``>>`` right
shift operators within the function to act exactly like Elixir pipes::

  from pipeop import pipes

  def add(a, b):
      return a + b

  def times(a, b):
      return a * b

  @pipes
  def calc()
      print 1 >> add(2) >> times(3)  # prints 9

Functions can have any number of arguments::

  def add3(a, b, c):
      return a + b + c

  @pipes
  def calc()
      print 1 >> add3(2, 3)  # prints 6

In Elixir libraries the first argument of a function is chosen with pipes in
mind but this is (obviously) not the case in Python - for instance the
enumerable args of ``map`` and ``reduce`` are first in their Elixir equivalents
but last in Python. For this reason I've also redefined the left shift operator
``<<`` to *append* it's left operand to the list of call arguments of the right
operand::

  def my_pow():
    print 2 >> pow(3)  # prints 8
    print 2 << pow(3)  # prints 9

Finally you can drop the braces for functions with a single argument::

    @pipes
    def sum(self):
        print [1, 2, 3] >> sum  # prints 6

There should be a small amount of processing overhead the first time the
function is called, otherwise there should be no difference to the
conventionally nested call code.

This is initial alpha code. It has been tested on Python 2.7.14 and 3.6.5 using
simple functions. Source line attributes are preserved so debuggers should be
able to follow the code as it executes. Pull requests and bug reports gratefully
accepted.

Robin Hilliard

*PS: Thanks to https://github.com/Stvad for submitting the first issue with some
great suggestions.*