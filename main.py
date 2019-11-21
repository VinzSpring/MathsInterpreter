import string
from math import *
from pprint import pprint
"""
< func_definition> ::= < name > ( <params> ) : <expression>

< assignment > ::= < name > = < expression >

< expression > ::= < term > + < expression > | < term > - < expression > | < term >

< term > ::= < factor > * < term > | < factor > / < term > | < factor >

< factor > ::= (< expression >) | < float > | < var > | < call >

"""

class RuntimeException(Exception):
    pass

def split_outer_levelx(s, m):
    i = 0
    indices = []
    for j, c in enumerate(s):
        if c == "(":
            i += 1
        elif c == ")":
            i -= 1
        elif i == 0 and c == m:
            indices.append(j)
    ls = []

    if len(indices) == 0:
        return [s]

    if len(indices) == 1:
        return s[:indices[0]], s[indices[0] + 1:]

    ls.append(s[:indices[0]])
    for i in range(len(indices) - 1):
        ls.append(s[indices[i] + len(m):indices[i+1]])
    ls.append(s[indices[-1] + len(m):])
    return ls


def split_outer_level(s, m):
    split = split_outer_levelx(s, m)
    if len(split) < 2:
        raise Exception("couldn't split into two!")
    if len(split) > 2:
        return split[0], m.join(split[1:])
    return split


class Fun:
    def __init__(self, body, arg_names):
        self.arg_names = arg_names
        self.body = body


class Scope:
    def __init__(self, **args):
        if "vars" in args:
            self.vars = args["vars"]
        else:
            self.vars = {}
        self.vars["PI"] = pi

        self.builtin_funcs = {
            "sin": lambda args: sin(args[0]),
            "cos": lambda args: cos(args[0]),
            "tan": lambda args: tan(args[0]),

            "asin": lambda args: asin(args[0]),
            "acos": lambda args: acos(args[0]),
            "atan": lambda args: atan(args[0]),
        }

        if "funcs" in args:
            self.funcs = args["funcs"]
        else:
            self.funcs = {}


def func_definition(input, scope: Scope):
    ls = input.split(":")
    name_args = ls[0].split("(")
    name = name_args[0]
    args = name_args[1][:-1].split(",")
    scope.funcs[name] = Fun(
        ls[1], args
    )


def assignment(input, scope: Scope):
    ls = input.split("=")
    name = ls[0]
    expression = ls[1]
    scope.vars[name] = expr(expression, scope)


def expr(input, scope: Scope):
    try:
        p1, p2 = split_outer_level(input, "+")
        return float(term(p1, scope)) + float(expr(p2, scope))
    except:
        pass
    try:
        p1, p2 = split_outer_level(input, "-")
        return float(term(p1, scope)) - float(expr(p2, scope))
    except:
        pass
    return term(input, scope)


def term(input, scope: Scope):
    try:
        p1, p2 = split_outer_level(input, "*")
        return float(factor(p1, scope)) * float(term(p2, scope))
    except:
        pass
    try:
        p1, p2 = split_outer_level(input, "/")
        return float(factor(p1, scope)) / float(term(p2, scope))
    except:
        pass
    return factor(input, scope)


def factor(input, scope: Scope):
    if input[0] == "(" and input[-1] == ")":
        return expr(input[1:-1], scope)
    elif input[-1] == ")" and input[0].lower() in string.ascii_lowercase:
        return call(input, scope)
    elif input[0].lower() in string.ascii_lowercase:
        return var(input, scope)
    return val(input, scope)


def val(input, scope: Scope):
    return float(input)


def call(input, scope: Scope):
    s_a = input.index("(")
    fn_name = input[:s_a]
    args = input[s_a:][1:-1]
    try:
        args = split_outer_levelx(args, ",")
    except:
        pass
    is_builtin_func = fn_name in scope.builtin_funcs
    is_custom_func = fn_name in scope.funcs
    if not (is_builtin_func or is_custom_func):
        raise RuntimeException("function '{}' not defined in scope!".format(fn_name))

    simplified = [None for i in range(len(args))]
    for i in range(len(args)):
        simplified[i] = expr(args[i], scope)

    if is_builtin_func:
        return val(scope.builtin_funcs[fn_name](simplified), scope)

    fn = scope.funcs[fn_name]
    vars = {}
    for i in range(len(fn.arg_names)):
        vars[fn.arg_names[i]] = simplified[i]
    return expr(fn.body, Scope(vars=vars, funcs=scope.funcs))


def var(input, scope: Scope):
    if input not in scope.vars:
        raise RuntimeException("use of undefined variable '{}'".format(input))
    return scope.vars[input]


class Runtime:
    def __init__(self):
        self.scope = Scope()
        self.shell_commands = {
            "ls vars": lambda: pprint(self.scope.vars),
            "ls funcs": lambda: pprint(["{}{}:{}\n".format(func_name, func.arg_names, func.body) for func_name, func in self.scope.funcs.items()]),
        }

    def execute_statements(self, code):
        for line in code.splitlines():
            self.execute_statement(line)

    def execute_statement(self, line):
        line = line.replace(" ", "").replace("\n", "").replace("\t", "")
        ops = [
            func_definition,
            assignment,
            expr
        ]
        for op in ops:
            try:
                res = op(line, self.scope)
                if res:
                    pprint(res)
                break
            except RuntimeException as e:
                pprint("ERROR: {}".format(str(e)))
            except:
                pass
        return self

    def start_shell(self):
        while True:
            line = input()
            if line == "exit()":
                break
            if line in self.shell_commands:
                self.shell_commands[line]()
            else:
                self.execute_statement(line)


if __name__ == "__main__":
    runtime = Runtime()
    runtime.start_shell()
