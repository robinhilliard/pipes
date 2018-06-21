from ast import parse, NodeTransformer, RShift, increment_lineno
from inspect import getsource
from textwrap import dedent


class _PipeTransformer(NodeTransformer):

    def visit_BinOp(self, node):
        if isinstance(node.op, RShift):
            # rewrite a >> b(...) as b(a, ...)
            node.right.args.insert(0, node.left)
            return self.visit(node.right)

        else:
            return node


def pipes(func):
    # name of our replacement function
    pipe_func_name = '__pipes_{}'.format(func.__code__.co_name)

    # variable context where decorator added
    ctx = func.__globals__

    # We only modify the function once
    if pipe_func_name not in ctx:
        # AST data structure representing parsed function code
        tree = parse(dedent(getsource(func)))

        # Fix line numbers so that debuggers still work
        increment_lineno(tree, func.__code__.co_firstlineno - 1)

        # Update name of function to compile
        tree.body[0].name = pipe_func_name

        # remove the pipe decorator so that we don't recursively call it again
        tree.body[0].decorator_list = \
            [d for d in tree.body[0].decorator_list if d.id != 'pipes']

        # Apply the visit_BinOp transformation
        tree = _PipeTransformer().visit(tree)

        # now compile the AST into an altered function definition
        code = compile(
            tree,
            filename=__file__,
            mode="exec")

        # and execute the definition in the original context
        exec(code, ctx)

    # return the modified function - original is never called
    return ctx[pipe_func_name]