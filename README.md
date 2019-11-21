# MathsRuntime
This is a simple monadic, recursive scripting environment for mathematical expressions.
# syntax

## shell comands:
- exit() exit shell
- ls vars list variables defined in global scope
- ls funcs list functions defined in global scope

## inbuilt functions:
- sin(x)
- cos(x)
- tan(x)
- asin(x)
- acos(x)
- atan(x)

## inbuilt constants:
- PI

## define custom functions
All functions are scoped.
Use recursion and it will never stop!
```
sum(a,b):a+b
//sum(1,2) -> 3.0

//override sum
sum(a,b,c):a+b+c

```

## example (interaction with shell)
```
a = 1+2
a
3.0
a=a*3
a
9.0
foo(a,b):sin(a)*b+1/2
foo(1,2)
2.182941969615793
b = sin(foo(1,2) * 12.45554) 
b
0.8841225885612423
ls funcs
["foo['a', 'b']:sin(a)*b+1/2\n"]
ls vars
{'PI': 3.141592653589793, 'a': 9.0, 'b': 0.8841225885612423}
b*a
7.95710329705118
a*a+a/2
85.5
foo(a,b,c):(a+b+c)/sin(PI)              
foo(1,2,3)
4.899371805958611e+16
```
