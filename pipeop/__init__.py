"""
   Implement a @pipes decorator that converts the << and >> operators
   to mimic Elixir pipes.
"""


from ast import Call, parse, Name, NodeTransformer, LShift, RShift, \
    increment_lineno, walk
from inspect import getsource, isclass, stack
from itertools import takewhile
from textwrap import dedent


class _PipeTransformer(NodeTransformer):

    def visit_BinOp(self, node):
        if isinstance(node.op, (LShift, RShift)):
            # Convert function name / lambda etc without braces into call
            if not isinstance(node.right, Call):
                return self.visit(Call(
                    func=node.right,
                    args=[node.left],
                    keywords=[],
                    starargs=None,
                    kwargs=None,
                    lineno=node.right.lineno,
                    col_offset=node.right.col_offset
                ))
            else:
                # Rewrite a >> b(...) as b(a, ...)
                node.right.args.insert(
                    0 if isinstance(node.op, RShift) else len(node.right.args),
                    node.left)
                return self.visit(node.right)

        else:
            return node


def pipes(func_or_class):
    if isclass(func_or_class):
        decorator_frame = stack()[1]
        ctx = decorator_frame[0].f_locals
        first_line_number = decorator_frame[2]

    else:
        ctx = func_or_class.__globals__
        first_line_number = func_or_class.__code__.co_firstlineno

    source = getsource(func_or_class)

    # AST data structure representing parsed function code
    tree = parse(dedent(source))

    # Fix line and column numbers so that debuggers still work
    increment_lineno(tree, first_line_number - 1)
    source_indent = sum([1 for _ in takewhile(str.isspace, source)]) + 1

    for node in walk(tree):
        if hasattr(node, "col_offset"):
            node.col_offset += source_indent

    # Update name of function or class to compile
    #tree.body[0].name = decorated_name

    # remove the pipe decorator so that we don't recursively
    # call it again. The AST node for the decorator will be a
    # Call if it had braces, and a Name if it had no braces.
    # The location of the decorator function name in these
    # nodes is slightly different.
    tree.body[0].decorator_list = \
        [d for d in tree.body[0].decorator_list
         if isinstance(d, Call) and d.func.id != 'pipes'
         or isinstance(d, Name) and d.id != 'pipes']

    # Apply the visit_BinOp transformation
    tree = _PipeTransformer().visit(tree)

    # now compile the AST into an altered function or class definition
    code = compile(
        tree,
        filename=ctx['__file__'],
        mode="exec")

    # and execute the definition in the original context so that the
    # decorated function can access the same scopes as the original
    exec(code, ctx)

    # return the modified function or class - original is never called
    return ctx[tree.body[0].name]
