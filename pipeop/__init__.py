from ast import Call, parse, Name, NodeTransformer, LShift, RShift, \
    increment_lineno
from inspect import getsource
from textwrap import dedent


class _PipeTransformer(NodeTransformer):

    def visit_BinOp(self, node):
        if isinstance(node.op, (LShift, RShift)):
            # Bare function name
            if isinstance(node.right, Name):
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


def pipes(func_or_cache_flag=True):

    def pipes_decorator(func):
        # name of our replacement function
        pipe_func_name = '__pipes_{}'.format(func.__code__.co_name)

        # variable context where decorator added
        ctx = func.__globals__

        # We only modify the function once
        if not func_or_cache_flag or pipe_func_name not in ctx:
            # AST data structure representing parsed function code
            tree = parse(dedent(getsource(func)))

            # Fix line numbers so that debuggers still work
            increment_lineno(tree, func.__code__.co_firstlineno - 1)

            # Update name of function to compile
            tree.body[0].name = pipe_func_name

            # remove the pipe decorator so that we don't recursively
            # call it again
            tree.body[0].decorator_list = \
                [d for d in tree.body[0].decorator_list
                 if isinstance(d, Call) and d.func.id != 'pipes'
                 or isinstance(d, Name) and d.id != 'pipes']

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

    if callable(func_or_cache_flag):
        # No arguments passed to @pipes so we received the function to wrap
        return pipes_decorator(func_or_cache_flag)

    else:
        # Cache argument was passed to @pipes, so return decorator, which
        # is in a closure with func_or_cache_flag set to True or False
        return pipes_decorator
