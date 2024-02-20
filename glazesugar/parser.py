"""
@author Shuji Kosuge
"""

import re
import ply.yacc as yacc
import ply.lex as lex
from . import CSP


tokens = [
    'INTEGER', 'SYMBOL', 'COMMENT',
    'DOMAIN', 'INT', 'BOOL',
    'ABS', 'NEG', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW', 'MIN', 'MAX', 'IF',
    'NOT', 'AND', 'OR', 'IMP', 'XOR', 'IFF',
    'FALSE', 'TRUE', 'EQ', 'NE', 'LE', 'LT', 'GE', 'GT',
    'ALLDIFFERENT'
]

literals = [';', '(', ')']


def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_DOMAIN(t):
    r'domain'
    return t


def t_INT(t):
    r'int'
    return t


def t_BOOL(t):
    r'bool'
    return t


def t_ABS(t):
    r'abs'
    return t


def t_NEG(t):
    r'neg'
    return t


def t_ADD(t):
    r'add|\+'
    return t


def t_SUB(t):
    r'sub|-'
    return t


def t_MUL(t):
    r'mul|\*'
    return t


def t_DIV(t):
    r'div|/'
    return t


def t_MOD(t):
    r'mod|%'
    return t


def t_POW(t):
    r'pow'
    return t


def t_MIN(t):
    r'min'
    return t


def t_MAX(t):
    r'max'
    return t


def t_IF(t):
    r'if\s'
    return t


def t_NOT(t):
    r'not|!\s'
    return t


def t_AND(t):
    r'and|&&'
    return t


def t_OR(t):
    r'or|\|\|'
    return t


def t_IMP(t):
    r'imp|=>'
    return t


def t_XOR(t):
    r'xor'
    return t


def t_IFF(t):
    r'iff'
    return t


def t_FALSE(t):
    r'false'
    return t


def t_TRUE(t):
    r'true'
    return t


def t_EQ(t):
    r'eq|='
    return t


def t_NE(t):
    r'ne|!='
    return t


def t_LE(t):
    r'le|<='
    return t


def t_LT(t):
    r'lt|<'
    return t


def t_GE(t):
    r'ge|>='
    return t


def t_GT(t):
    r'gt|>'
    return t


def t_ALLDIFFERENT(t):
    r'alldifferent'
    return t


def t_COMMENT(t):
    r';[^\n]*|/\*[\s\S]*?\*/'
    t.lineno += t.value.count('\n')


def t_SYMBOL(t):
    r'[A-Za-z0-9_\.+\-*/%=<>!&|]+'
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lineno += t.value.count("\n")


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def p_expr_list(p):
    """
    expr_list : expr_list expr
    """
    if p[2]:
        global parser_csp
        parser_csp.add(p[2])


def p_expr_list_base(p):
    """
    expr_list :
    """
    p[0] = []


def p_domain_definition(p):
    """
    expr : '(' DOMAIN domain_name lower_bound upper_bound ')'
         | '(' DOMAIN domain_name '(' range_list ')' ')'
         | '(' DOMAIN domain_name value ')'
    """
    if len(p) == 7:
        p[0] = CSP.Domain(p[4], p[5])
    elif len(p) == 8:
        p[0] = CSP.Domain(p[5])
    else:
        p[0] = CSP.Domain(p[4])


def p_domain_name(p):
    """
    domain_name : SYMBOL
    """
    p[0] = p[1]


def p_lower_bound(p):
    """
    lower_bound : INTEGER
    """
    p[0] = p[1]


def p_upper_bound(p):
    """
    upper_bound : INTEGER
    """
    p[0] = p[1]


def p_value(p):
    """
    value : INTEGER
    """
    p[0] = p[1]


def p_range_list(p):
    """
    range_list : range_list range
               | range
    """
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


def p_range(p):
    """
    range : INTEGER
          | '(' INTEGER INTEGER ')'
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [i for i in range(p[2], p[3]+1)]


def p_integer_variable_definition(p):
    """
    expr : '(' INT integer_variable_name domain_name ')'
         | '(' INT integer_variable_name lower_bound upper_bound ')'
         | '(' INT integer_variable_name '(' range_list ')' ')'
         | '(' INT integer_variable_name value ')'
    """
    global parser_csp
    if len(p) == 6:
        raise ValueError("No domain Error")
    elif len(p) == 7:
        parser_csp.int(CSP.Var(p[3]), CSP.Domain(p[4], p[5]))
    elif len(p) == 8:
        parser_csp.int(CSP.Var(p[3]), CSP.Domain(p[5]))
    else:
        parser_csp.int(CSP.Var(p[3]), CSP.Domain(p[4]))


def p_integer_variable_name(p):
    """
    integer_variable_name : SYMBOL
    """
    p[0] = p[1]


def p_boolean_variable_definition(p):
    """
    expr : '(' BOOL boolean_variable_name ')'
    """
    global parser_csp
    parser_csp.bool(CSP.Bool(p[3]))


def p_boolean_variable_name(p):
    """
    boolean_variable_name : SYMBOL
    """
    p[0] = p[1]


def p_term(p):
    """
    expr : term
    """
    p[0] = p[1]


def p_term_list_base(p):
    """
    term_list :
    """
    p[0] = []


def p_term_list(p):
    """
    term_list : term_list term
    """
    p[1].append(p[2])
    p[0] = p[1]


def p_term_integer(p):
    """
    term : INTEGER
    """
    p[0] = p[1]


def p_term_integer_variable_name(p):
    """
    term : integer_variable_name
    """
    p[0] = p[1]


def p_term_abs(p):
    """
    term : '(' ABS term ')'
    """
    p[0] = CSP.Abs(p[3])


def p_term_neg(p):
    """
    term : '(' NEG term ')'
         | '(' SUB term ')'
    """
    p[0] = CSP.Neg(p[3])


def p_term_add(p):
    """
    term : '(' ADD ')'
         | '(' ADD term_list ')'
    """

    if len(p) == 4:
        p[0] = CSP.Add()
    else:
        p[0] = CSP.Add(*p[3])


def p_term_sub(p):
    """
    term : '(' SUB term term_list ')'
    """
    p[0] = CSP.Sub(p[3], *p[4])


def p_term_mul(p):
    """
    term : '(' MUL term term ')'
    """
    p[0] = CSP.Mul(p[3], p[4])


def p_term_div(p):
    """
    term : '(' DIV term term ')'
    """
    p[0] = CSP.Div(p[3], p[4])


def p_term_mod(p):
    """
    term : '(' MOD term term ')'
    """
    p[0] = CSP.Mod(p[3], p[4])


def p_term_pow(p):
    """
    term : '(' POW term term ')'
    """
    raise ValueError("pow is not supported.")
    # p[0] = CSP.Pow(p[3], p[4])


def p_term_min(p):
    """
    term : '(' MIN term term ')'
    """
    p[0] = CSP.Min(p[3], p[4])


def p_term_max(p):
    """
    term : '(' MAX term term ')'
    """
    p[0] = CSP.Max(p[3], p[4])


def p_term_if(p):
    """
    term : '(' IF logical_formula term term ')'
    """
    p[0] = CSP.Ite(p[3], p[4], p[5])


def p_constraint(p):
    """
    expr : constraint
    """
    p[0] = p[1]


def p_constraint_logical_formula(p):
    """
    constraint : logical_formula
    """
    p[0] = p[1]


def p_constraint_logical_formula_list_base(p):
    """
    logical_formula_list :
    """
    p[0] = []


def p_constraint_list(p):
    """
    logical_formula_list : logical_formula_list logical_formula
    """
    p[1].append(p[2])
    p[0] = p[1]


def p_constraint_atomic_formula(p):
    """
    logical_formula : atomic_formula
    """
    p[0] = p[1]


def p_constraint_not(p):
    """
    logical_formula : '(' NOT logical_formula ')'
    """
    p[0] = CSP.Not(p[3])


def p_constraint_AND(p):
    """
    logical_formula : '(' AND ')'
                    | '(' AND logical_formula_list ')'
    """
    if len(p) == 4:
        p[0] = CSP.And()
    else:
        p[0] = CSP.And(*p[3])


def p_constraint_OR(p):
    """
    logical_formula : '(' OR ')'
                    | '(' OR logical_formula_list ')'
    """
    if len(p) == 4:
        p[0] = CSP.Or()
    else:
        p[0] = CSP.Or(*p[3])


def p_constraint_imp(p):
    """
    logical_formula : '(' IMP logical_formula logical_formula ')'
    """
    p[0] = CSP.Imp(p[3], p[4])


def p_constraint_xor(p):
    """
    logical_formula : '(' XOR logical_formula logical_formula ')'
    """
    p[0] = CSP.Xor(p[3], p[4])


def p_constraint_iff(p):
    """
    logical_formula : '(' IFF logical_formula logical_formula ')'
    """
    p[0] = CSP.Iff(p[3], p[4])


def p_constraint_false(p):
    """
    atomic_formula : FALSE
    """
    p[0] = CSP.FALSE()


def p_constraint_true(p):
    """
    atomic_formula : TRUE
    """
    p[0] = CSP.TRUE()


def p_constraint_boolean_variable_name(p):
    """
    atomic_formula : boolean_variable_name
    """
    p[0] = p[1]


def p_constraint_eq(p):
    """
    atomic_formula : '(' EQ term term ')'
    """
    p[0] = CSP.Eq(p[3], p[4])


def p_constraint_ne(p):
    """
    atomic_formula : '(' NE term term ')'
    """
    p[0] = CSP.Ne(p[3], p[4])


def p_constraint_le(p):
    """
    atomic_formula : '(' LE term term ')'
    """
    p[0] = CSP.Le(p[3], p[4])


def p_constraint_lt(p):
    """
    atomic_formula : '(' LT term term ')'
    """
    p[0] = CSP.Lt(p[3], p[4])


def p_constraint_ge(p):
    """
    atomic_formula : '(' GE term term ')'
    """
    p[0] = CSP.Ge(p[3], p[4])


def p_constraint_gt(p):
    """
    atomic_formula : '(' GT term term ')'
    """
    p[0] = CSP.Gt(p[3], p[4])


def p_constraint_alldifferent_constraint(p):
    """
    atomic_formula : alldifferent_constraint
    """
    p[0] = p[1]


def p_constraint_alldifferent(p):
    """
    alldifferent_constraint : '(' ALLDIFFERENT ')'
                            | '(' ALLDIFFERENT term_list ')'
                            | '(' ALLDIFFERENT '(' ')' ')'
                            | '(' ALLDIFFERENT '(' term_list ')' ')'
    """
    if len(p) == 5:
        p[0] = CSP.Alldifferent(*p[3])
    elif len(p) == 6:
        p[0] = CSP.Alldifferent(*p[4])
    else:
        p[0] = CSP.Alldifferent()


def p_error(p):
    print(f"Syntax error at '{p.value}' (type: {p.type}) on line {p.lineno}")


parser_csp = CSP.CSP()
lexer = lex.lex()
parser = yacc.yacc()


def read_csp(csp_str) -> CSP:
    global parser
    parser.parse(csp_str)
    return parser_csp

