
import ply.yacc as yacc
import ply.lex as lex
from Lexico import tokens, lexer, errores, find_column
from Expressions.Aritmetica import *
from Expressions.Primitivo import Primitivo
from Instructions.ImprimirClg import ImprimirClg
from Expressions.Logica import *
from Expressions.Relacional import *

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),
    ('left', 'IGUALIGUAL', 'DISTINTO'),
    ('left', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV', 'MOD'),
    ('left', 'POT'),
    ('right', 'UMENOS')
)

def p_init(t):
    '''init            : instrucciones'''
    t[0] = t[1]

def p_instrucciones_lista(t):
    '''instrucciones    : instrucciones instruccion
                        | instruccion'''
    if len(t) != 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion      : console_inst PCOMA
                        '''
    t[0] = t[1]

def p_console_inst(t):
    'console_inst : RCONSOLE PUNTO RLOG PARA expresion PARC'
    t[0] = ImprimirClg(t[5], t.lineno(1), find_column(input, t.slice[1]))

# Expresiones
def p_expresion_aritmetica(t):
    '''expresion : expresion MAS expresion
                | expresion MENOS expresion
                | expresion POR expresion
                | expresion DIV expresion
                | expresion MOD expresion
                | expresion POT expresion
                | MENOS expresion %prec UMENOS'''
    
    if t[2] == '+'  : 
        t[0] = Aritmetica(t[1], t[3], TipoOperacionAritmetica.SUMA, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(t[1], t[3], TipoOperacionAritmetica.RESTA, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*': 
        t[0] = Aritmetica(t[1], t[3], TipoOperacionAritmetica.MULTI, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/': 
        t[0] = Aritmetica(t[1], t[3], TipoOperacionAritmetica.DIV, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%': 
        t[0] = Aritmetica(t[1], t[3], TipoOperacionAritmetica.MOD, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^': 
        t[0] = Aritmetica(t[1], t[3], TipoOperacionAritmetica.POT, t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_logica(t):
    '''expresion : expresion OR expresion
                 | expresion AND expresion
                 | NOT expresion %prec UNOT'''
    
    if t[2] == '||':
        t[0] = Logica(t[1], t[3], TipoLogicas.OR, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(t[1], t[3], TipoLogicas.AND, t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == '!':
        t[0] = Logica(t[2], t[2], TipoLogicas.NOT, t.lineno(2), find_column(input, t.slice[1]))

def p_expresion_relacional(t):
    '''expresion : expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MAYORIGUAL expresion
                 | expresion MENORIGUAL expresion
                 | expresion DISTINTO expresion
                 | expresion IGUALIGUAL expresion'''
    
    if t[2] == '<':
        t[0] = Relacional(t[1], t[3], TipoRelacionales.MENOR, t.lineno(2), find_column(input, t.slice[2]))
    if t[2] == '>':
        t[0] = Relacional(t[1], t[3], TipoRelacionales.MAYOR, t.lineno(2), find_column(input, t.slice[2]))
    if t[2] == '<=':
        t[0] = Relacional(t[1], t[3], TipoRelacionales.MENORIGUAL, t.lineno(2), find_column(input, t.slice[2]))
    if t[2] == '>=':
        t[0] = Relacional(t[1], t[3], TipoRelacionales.MAYORIGUAL, t.lineno(2), find_column(input, t.slice[2]))
    if t[2] == '===':
        t[0] = Relacional(t[1], t[3], TipoRelacionales.IGUALIGUAL, t.lineno(2), find_column(input, t.slice[2]))
    if t[2] == '!==':
        t[0] = Relacional(t[1], t[3], TipoRelacionales.DISTINTO, t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_primitivos(t):
    '''expresion : ENTERO
                 | DECIMAL
                 | ID
                 | CADENA
                 | RTRUE
                 | RFALSE'''
    
    if t.slice[1].type == 'ENTERO':
        t[0] = Primitivo(Tipo.NUMBER, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'DECIMAL':
        t[0] = Primitivo(Tipo.NUMBER, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'ID':
        t[0] = Primitivo(Tipo.STRING, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'CADENA':
        t[0] = Primitivo(Tipo.STRING, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'RTRUE':
        t[0] = Primitivo(Tipo.BOOL, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'RFALSE':
        t[0] = Primitivo(Tipo.BOOL, t[1], t.lineno(1), find_column(input, t.slice[1]))
    
def p_error(t):
    print(" Error sintáctico en '%s'" % t.value)

#parser = yacc.yacc()

input = ''

def parse(inp):
    global errores
    global parser
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    lexer.lineno = 1
    return parser.parse(inp)

# entrada = '''console.log(3 + 6);
#         console.log(3 + 10);
#         console.log(3 + 4);'''

# instrucciones = parse(entrada)

# for inst in instrucciones:
#     inst.ejecutar(None)