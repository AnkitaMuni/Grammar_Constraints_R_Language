import ply.yacc as yacc
from r_lexer import tokens

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = p[1] + [p[2]] if p[2] is not None else p[1]

def p_statement(p):
    '''statement : if_statement
                 | for_statement
                 | while_statement
                 | expression
                 | assignment_statement
                 | statement SEMICOLON'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1]  

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'''
    if len(p) == 8:
        p[0] = {'type': 'if', 'condition': p[3], 'body': p[6]}
    else:
        p[0] = {'type': 'if', 'condition': p[3], 'body': p[6], 'else_body': p[10]}

def p_for_statement(p):
    '''for_statement : FOR LPAREN ID IN expression COLON expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = {'type': 'for', 'variable': p[3], 'start': p[5], 'end': p[7], 'body': p[10]}

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = {'type': 'while', 'condition': p[3], 'body': p[6]}

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression'''
    p[0] = {'type': 'assignment', 'variable': p[1], 'value': p[3]}

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term
                  | expression TIMES term
                  | expression DIVIDE term
                  | expression MODULO term
                  | expression POWER term
                  | expression EQ term
                  | expression NEQ term
                  | expression LT term
                  | expression GT term
                  | expression LTE term
                  | expression GTE term
                  | PRINT LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == 'print':
        p[0] = {'type': 'print', 'expression': p[3]}
    else:
        p[0] = {'type': 'binary_op', 'op': p[2], 'left': p[1], 'right': p[3]}

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor
            | term MODULO factor
            | term POWER factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'type': 'binary_op', 'op': p[2], 'left': p[1], 'right': p[3]}

def p_factor(p):
     '''factor : NUMBER
              | STRING
              | ID
              | LPAREN expression RPAREN'''
     p[0] = p[1]

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")
    else:
        raise SyntaxError("Syntax error: Unexpected end of input")

parser = yacc.yacc()

def parse(data):
    result = parser.parse(data)
    if result is None:
        raise SyntaxError("Invalid syntax")
    return result

__all__ = ['parse']