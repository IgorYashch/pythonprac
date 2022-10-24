from math import *

functions_dict = {}

def create_function(params, expr):
    
    def function(*vals):
        vars_definition = ''.join(
            ['{}={};'.format(param_name, val) for param_name, val in zip(params, vals)]
        )
        exec(vars_definition)
        return eval(expr)

    return function 

functions_dict['quit'] = create_function(
    ('s', 'k', 'n'), 
    's.format(k, n)'
)

k = 1
n = 0

while s := input():
    n += 1
    if s[0] == ':':
        k += 1
        # Определение функции
        name, *params, expr = s[1:].split()
        functions_dict[name] = create_function(params, expr)
    
    elif s[:4] == 'quit':
        # Выход
        val = s[4:].strip()
        print(functions_dict['quit'](val, k, n))
        break

    else:
        # Выполнение функции
        name, *vals = s.split()
        print(functions_dict[name](*vals))