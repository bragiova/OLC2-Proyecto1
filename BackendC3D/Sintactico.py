
import ply.yacc as yacc
import ply.lex as lex
from Lexico import tokens, lexer, find_column
from Expressions.Aritmetica import *
from Expressions.Primitivo import Primitivo
from Instructions.ImprimirClg import ImprimirClg
from Expressions.Logica import *
from Expressions.Relacional import *
from Instructions.Declaracion import Declaracion
from Expressions.Identificador import Identificador
from Instructions.Asignacion import Asignacion
from Instructions.If import If
from Instructions.For import For
from Instructions.While import While
from Instructions.Funcion import Funcion
from Instructions.ParametroFuncion import ParametroFuncion
from Expressions.LlamadaFuncion import LlamadaFuncion
from Instructions.Return import Return
from Instructions.Break import Break
from Instructions.Continue import Continue
from Nativas.UpperCase import UpperCase
from Nativas.LowerCase import LowerCase
from Nativas.String import ToString
from Nativas.Fixed import ToFixed
from Nativas.Exponential import ToExponential
from Nativas.TypeOf import TypeOf
from Nativas.Length import Length
from Sym.TablaSimbolos import *

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),
    ('left', 'IGUALIGUAL', 'DISTINTO'),
    ('left', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left', 'MAS', 'MENOS', 'COMA'),
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
                        | declaracion_inst PCOMA
                        | asignacion_inst PCOMA
                        | if_inst PCOMA
                        | for_inst PCOMA
                        | llamada_func PCOMA
                        | return_inst PCOMA
                        | break_inst PCOMA
                        | continue_inst PCOMA
                        '''
    t[0] = t[1]

def p_instruccion_t(t):
    '''instruccion      : console_inst
                        | declaracion_inst
                        | asignacion_inst
                        | if_inst
                        | for_inst
                        | while_inst
                        | funcion_inst
                        | llamada_func
                        | return_inst
                        | break_inst
                        | continue_inst
                        '''
    t[0] = t[1]

# console.log
def p_console_inst(t):
    'console_inst : RCONSOLE PUNTO RLOG PARA expresion_list PARC'
    t[0] = ImprimirClg(t[5], t.lineno(1), find_column(input, t.slice[1]))

# Declaración
def p_declaracion_inst(t):
    '''declaracion_inst : RLET ID DPUNTOS tipo IGUAL expresion
                        | RLET ID DPUNTOS tipo'''
    if len(t) == 5:
        t[0] = Declaracion(t[2], None, t[4], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Declaracion(t[2], t[6], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo(t):
    '''declaracion_inst : RLET ID IGUAL expresion
                        | RLET ID'''
    if len(t) == 3:
        t[0] = Declaracion(t[2], None, Tipo.ANY, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Declaracion(t[2], t[4], Tipo.ANY, t.lineno(1), find_column(input, t.slice[1]))

# Asignación
def p_asignacion_inst(t):
    'asignacion_inst : ID IGUAL expresion'
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

# IF
def p_if_inst(t):
    'if_inst : RIF if_cond'
    t[0] = t[2]

def p_if_cond(t):
    'if_cond : expresion LLAVEA instrucciones LLAVEC'
    t[0] = If(t[1], t[3], None, None, t.lineno(2), find_column(input, t.slice[2]))

def p_if_else(t):
    'if_cond : expresion LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    t[0] = If(t[1], t[3], t[7], None, t.lineno(2), find_column(input, t.slice[2]))

def p_else_if(t):
    'if_cond : expresion LLAVEA instrucciones LLAVEC RELSE RIF if_cond'
    t[0] = If(t[1], t[3], None, t[7], t.lineno(2), find_column(input, t.slice[2]))

# For
def p_for(t):
    'for_inst : RFOR PARA declaracion_inst PCOMA expresion PCOMA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = For(t[3], t[5], t[7], t[10], t.lineno(1), find_column(input, t.slice[1]))

# While
def p_while_inst(t):
    'while_inst : RWHILE expresion LLAVEA instrucciones LLAVEC'
    t[0] = While(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

# Funciones
def p_funcion_inst(t):
    '''funcion_inst : RFUNCTION ID PARA PARC LLAVEA instrucciones LLAVEC
                    | RFUNCTION ID PARA PARC DPUNTOS tipo LLAVEA instrucciones LLAVEC'''
    if len(t) == 8:
        t[0] = Funcion(t[2], [], t[6], Tipo.ANY, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Funcion(t[2], [], t[8], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_param(t):
    '''funcion_inst : RFUNCTION ID PARA list_params PARC LLAVEA instrucciones LLAVEC
                    | RFUNCTION ID PARA list_params PARC DPUNTOS tipo LLAVEA instrucciones LLAVEC'''
    if len(t) == 9:
        t[0] = Funcion(t[2], t[4], t[7], Tipo.ANY, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Funcion(t[2], t[4], t[9], t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_list_params(t):
    '''list_params : list_params COMA parametro
                   | parametro'''
    if len(t) != 2:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_parametro(t):
    '''parametro : ID DPUNTOS tipo
                 | ID'''
    if len(t) == 2:
        t[0] = ParametroFuncion(t[1], Tipo.ANY, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = ParametroFuncion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_return_inst(t):
    '''return_inst : RRETURN
                   | RRETURN expresion'''
    if len(t) == 2:
        t[0] =  Return(None, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] =  Return(t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_break_inst(t):
    'break_inst : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

def p_continue_inst(t):
    'continue_inst : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))

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
    elif t[1] == '-':
        valorNeg = Primitivo(Tipo.NUMBER, 0, t.lineno(1), find_column(input, t.slice[1]))
        t[0] = Aritmetica(valorNeg, t[2], TipoOperacionAritmetica.RESTA, t.lineno(1), find_column(input, t.slice[1]))

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

def p_expresion_parentesis(t):
    'expresion : PARA expresion PARC'
    t[0] = t[2]

def p_llamada_funcion(t):
    'llamada_func : ID PARA PARC'
    t[0] = LlamadaFuncion(t[1], [], t.lineno(1), find_column(input, t.slice[1]))

def p_llamada_func_param(t):
    'llamada_func : ID PARA expresion_list PARC'
    t[0] = LlamadaFuncion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_list(t):
    '''expresion_list : expresion_list COMA expresion
                      | expresion'''
    if len(t) != 2:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_expresion_primitivos(t):
    '''expresion : ENTERO
                 | DECIMAL
                 | ID
                 | CADENA
                 | RTRUE
                 | RFALSE
                 | RNULL'''
    
    if t.slice[1].type == 'ENTERO':
        t[0] = Primitivo(Tipo.NUMBER, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'DECIMAL':
        t[0] = Primitivo(Tipo.NUMBER, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'ID':
        t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'CADENA':
        t[0] = Primitivo(Tipo.STRING, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'RTRUE':
        t[0] = Primitivo(Tipo.BOOL, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'RFALSE':
        t[0] = Primitivo(Tipo.BOOL, t[1], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'RNULL':
        t[0] = Primitivo(Tipo.NULL, t[1], t.lineno(1), find_column(input, t.slice[1]))
    
def p_expresion_incdec(t):
    '''expresion : expresion MAS MAS
                 | expresion MENOS MENOS'''
    if t[2] == '+':
        incrementable = Primitivo(Tipo.NUMBER, 1, t.lineno(2), find_column(input, t.slice[2]))
        t[0] = Aritmetica(t[1], incrementable, TipoOperacionAritmetica.SUMA, t.lineno(2), find_column(input, t.slice[2]))
    else:
        decrementable = Primitivo(Tipo.NUMBER, 1, t.lineno(2), find_column(input, t.slice[2]))
        t[0] = Aritmetica(t[1], decrementable, TipoOperacionAritmetica.RESTA, t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_func(t):
    'expresion : llamada_func'
    t[0] = t[1]

def p_expresion_nativas(t):
    'expresion : nativa_exp'
    t[0] = t[1]

def p_tipo(t):
    '''tipo : RNUMBER
            | RSTRING
            | RBOOLEAN
            | RANY'''
    if t.slice[1].type == 'RNUMBER':
        t[0] = Tipo.NUMBER
    elif t.slice[1].type == 'RSTRING':
        t[0] = Tipo.STRING
    elif t.slice[1].type == 'RBOOLEAN':
        t[0] = Tipo.BOOL
    elif t.slice[1].type == 'RANY':
        t[0] = Tipo.ANY

def p_nativas(t):
    '''nativa_exp : expresion PUNTO RUPCASE PARA PARC
                  | expresion PUNTO RLOWCASE PARA PARC
                  | expresion PUNTO RTOSTRING PARA PARC
                  | RSTRINGN PARA expresion PARC
                  | expresion PUNTO RFIXED PARA expresion PARC
                  | expresion PUNTO REXPONENTIAL PARA expresion PARC
                  | RTYPEOF PARA expresion PARC
                  | RLENGTH PARA expresion PARC'''
    if t.slice[3].type == 'RUPCASE':
        t[0] = UpperCase(t[1], t.lineno(3), find_column(input, t.slice[3]))
    elif t.slice[3].type == 'RLOWCASE':
        t[0] = LowerCase(t[1], t.lineno(3), find_column(input, t.slice[3]))
    elif t.slice[3].type == 'RTOSTRING':
        t[0] = ToString(t[1], t.lineno(3), find_column(input, t.slice[3]))
    elif t.slice[1].type == 'RSTRINGN':
        t[0] = ToString(t[3], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[3].type == 'RFIXED':
        t[0] = ToFixed(t[1], t[5], t.lineno(3), find_column(input, t.slice[3]))
    elif t.slice[3].type == 'REXPONENTIAL':
        t[0] = ToExponential(t[1], t[5], t.lineno(3), find_column(input, t.slice[3]))
    elif t.slice[1].type == 'RTYPEOF':
        t[0] = TypeOf(t[3], t.lineno(1), find_column(input, t.slice[1]))
    elif t.slice[1].type == 'RLENGTH':
        t[0] = Length(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_error(t):
    
    if t is not None:
        print(" Error sintáctico en '%s'" % t.value)
        if t.type == 'error':
            errLexSin = Error('Léxico', 'Caracter ' + str(t.value)[0] + ' no reconocido en el lenguaje', t.lexer.lineno, find_column(input, t))
        else:
            errLexSin = Error('Sintáctico', 'Error sintáctico en ' + str(t.value), t.lexer.lineno, find_column(input, t))
        parser.errok()
        TablaSimbolos.errores.append(errLexSin)
        
#parser = yacc.yacc()

input = ''

def parse(inp):
    # global errores
    global parser
    # errores = []
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