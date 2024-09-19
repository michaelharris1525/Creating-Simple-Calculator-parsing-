from pair import *
from operator import add, sub, mul, truediv

# def is_float(character):
#     try: 
#         float(character)
#         return True
#     except ValueError:
#         return False

def tokenize(expression):
    """ Takes a string and returns a list where each item
    in the list is a parenthesis, one of the four operators (/, *, -, +),
    or a number literal.
    >>> tokenize("(+ 3 2)")
    ['(', '+', '3', '2', ')']
    >>> tokenize("(- 9 3 3)")
    ['(', '-', '9', '3', '3', ')']
    >>> tokenize("(+ 10 100)")
    ['(', '+', '10', '100', ')']
    >>> tokenize("(+ 5.5 10.5)")
    ['(', '+', '5.5', '10.5', ')']
    >>> expr = "(* (- 8 4) 4)"
    >>> tokenize(expr)
    ['(', '*', '(', '-', '8', '4', ')', '4', ')']
    >>> expr = "(* (- 6 8) (/ 18 3) (+ 10 1 2))"
    >>> tokenize(expr)
    ['(', '*', '(', '-', '6', '8', ')', '(', '/', '18', '3', ')', '(', '+', '10', '1', '2', ')', ')']
    """
    # Write your code here
    # new_expression = expression.replace("(", "( ").replace(")", " )").split()
    # return new_expression


    # empty_list = []
    # for char in expression :
    #     if char in ('(', ')', '+', '-', '/', '*'):
    #         empty_list.append(char)
    #     elif is_float(char) == True:
    #         empty_list.append(char)
    #     elif char.isdigit() == True:
    #         empty_list.append(char)

    s = ""
    for char in expression:
        if char == "(":
            s += "( "
        elif char == ")" :
            s += " )"
        else:
            s += char
    return s.split()
        

        




# OPTIONAL
def parse_tokens(tokens, index):
    """ Takes a list of tokens and an index and converts the tokens to a Pair list

    >>> parse_tokens(['(', '+', '1', '1', ')'], 0)
    (Pair('+', Pair(1, Pair(1, nil))), 5)
    >>> parse_tokens(['(', '*', '(', '-', '8', '4', ')', '4', ')'], 0)
    (Pair('*', Pair(Pair('-', Pair(8, Pair(4, nil))), Pair(4, nil))), 9)
    """
    # Write your code here
    if tokens[index] == "(":
        operator = tokens[index + 1]
        if index != 0 :
            new_pair, index = parse_tokens(tokens, index + 2)
            operator = Pair(operator, new_pair)
        if index == 0:
            index += 2
        new_pair, index = parse_tokens(tokens, index)
        return Pair(operator, new_pair), index
    if tokens[index] == ")" :
        return nil, index + 1
    try:
        if "." in tokens[index] :
            number = float(tokens[index])
        else: 
            number = int(tokens[index])
        new_pair, index = parse_tokens(tokens, index + 1)
        return Pair(number, new_pair), index

    except ValueError as e: 
        raise TypeError("This is an error for values.... check values again")
    

def parse(tokens) :
    tokenize, index = parse_tokens(tokens, 0)
    return tokenize

def reduce(func, operands, initial) :
    # while its not empty
    while operands is not nil:
        initial = func(initial, operands.first)
        operands = operands.rest 
    return initial

def apply(operator, operands) : 
        if operator == '+' :
            return reduce(add, operands, 0)
        elif operator == '*':
            return reduce(mul, operands, 1)
    
        elif operator == '-':
            return reduce(sub, operands.rest, operands.first)

        elif operator == '/':
            return reduce(truediv, operands.rest, operands.first)
        else:
            raise TypeError("invalid operator...in the apply function")

def eval(syntax_tree):
    
    if isinstance(syntax_tree, (int,float)):
        return syntax_tree
    elif isinstance(syntax_tree, Pair) :
        if isinstance(syntax_tree.first, Pair) :
            new = eval(syntax_tree.first)
            last = syntax_tree.rest.map(eval) 
            return Pair(new, last)
        else:
            new = syntax_tree.rest.map(eval)
            return apply(syntax_tree.first, new)
        
    else:
        raise TypeError("Invalid Operator...Evaluate again")
    



if __name__ == "__main__":
#   main loop should use this greeting over and over
    print("Welcome to the CS 111 Calculator Interpreter.")
    while True:
        expression = input("calc >> ")
    
        if expression.lower() == "exit":
            break
        tokens = tokenize(expression)

        try:
            tree = parse(tokens)
            answer = eval(tree)
            print(answer)
        except BaseException as e:
            print(e)

    print("Goodbye!")