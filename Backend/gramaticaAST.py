import ply.yacc as yacc
import ply.lex as lex
import sys

from NodoAST.Nodo import Nodo

reservadas = {
    'null' : 'RNULL',
    'number' : 'RNUMBER',
    'boolean' : 'RBOOLEAN',
    'string' : 'RSTRING',
    'String' : 'RSTRINGN',
    'any' : 'RANY',
    'interface' : 'RINTERFACE',
    'function' : 'RFUNCTION',
    'toFixed' : 'RFIXED',
    'toExponential' : 'REXPONENTIAL',
    'toString' : 'RTOSTRING',
    'toLowerCase' : 'RLOWCASE',
    'toUpperCase' : 'RUPCASE',
    'split' : 'RSPLIT',
    'concat' : 'RCONCAT',
    'console' : 'RCONSOLE',
    'log': 'RLOG',
    'let' : 'RLET',
    'if' : 'RIF',
    'else' : 'RELSE',
    'while' : 'RWHILE',
    'for' : 'RFOR',
    'of' : 'ROF',
    'in' : 'RIN',
    'break' : 'RBREAK',
    'continue' : 'RCONTINUE',
    'return' : 'RRETURN',
    'true' : 'RTRUE',
    'false' : 'RFALSE',
    'typeof' : 'RTYPEOF',
    'length' : 'RLENGTH',
}

tokens = [
    'COMA',
    'PCOMA',
    'PUNTO',
    'DPUNTOS',
    'LLAVEA',
    'LLAVEC',
    'PARA',
    'PARC',
    'CORA',
    'CORC',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POT',
    'MOD',
    'IGUAL',
    'IGUALIGUAL',
    'DISTINTO',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'OR',
    'AND',
    'NOT',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'ID',
] + list(reservadas.values())

# Tokens
t_COMA = r','
t_PCOMA = r';'
t_DPUNTOS = r':'
t_PUNTO = r'\.'
t_LLAVEA = r'\{'
t_LLAVEC = r'\}'
t_PARA = r'\('
t_PARC = r'\)'
t_CORA = r'\['
t_CORC = r'\]'
t_MAS = r'\+'
t_MENOS = r'\-'
t_POR = r'\*'
t_DIV = r'\/'
t_POT = r'\^'
t_MOD = r'\%'
t_IGUAL = r'\='
t_IGUALIGUAL = r'\==='
t_DISTINTO = r'\!=='
t_MAYOR = r'\>'
t_MENOR = r'\<'
t_MAYORIGUAL = r'\>='
t_MENORIGUAL = r'\<='
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'\!'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Valor Decimal muy grande %d", t.value)
        t.value = 0.0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor Entero muy grande %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t


def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # remueve las comillas
    t.value = t.value.replace('\\t','\t')
    t.value = t.value.replace('\\n','\n')
    t.value = t.value.replace('\\"','\"')
    t.value = t.value.replace("\\'","\'")
    t.value = t.value.replace('\\\\','\\')
    return t

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple # ...
def t_COMENTARIO_SIMPLE(t):
    r'\/\/.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

#Error
def t_error(t):
    print('lexico ' + t.value[0], input)
    t.lexer.skip(1)

def find_column(inp, tk):
    line_start = inp.rfind('\n', 0, tk.lexpos) + 1
    return (tk.lexpos - line_start) + 1

lexer = lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),
    ('left', 'IGUALIGUAL', 'DISTINTO'),
    ('left', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left', 'MAS', 'MENOS', 'COMA'),
    ('left', 'POR', 'DIV', 'MOD'),
    ('left', 'PARA', 'PARC'),
    ('left', 'POT'),
    ('right', 'UMENOS')
)

def p_init(t):
    '''init            : instrucciones'''
    nodoInit = Nodo('Inicio')
    nodoInit.insertHijo(t[1])
    t[0] = nodoInit.getGrafoAST()

def p_instrucciones_lista(t):
    '''instrucciones    : instrucciones instruccion
                        | instruccion'''
    nodoInstrucciones = Nodo('instrucciones')
    if len(t) != 2:
        nodoInstrucciones.insertHijo(t[2])
        nodoInstrucciones.insertHijo(t[1])
        t[0] = nodoInstrucciones
    else:
        nodoInstrucciones.insertHijo(t[1])
        t[0] = nodoInstrucciones

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
    nodoInstruccion = Nodo('instruccion')
    nodoInstruccion.insertHijo(t[1])
    t[0] = nodoInstruccion

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
    nodoInstruccion = Nodo('instruccion')
    nodoInstruccion.insertHijo(t[1])
    t[0] = nodoInstruccion

# console.log
def p_console_inst(t):
    'console_inst : RCONSOLE PUNTO RLOG PARA expresion_list PARC'
    nodoImprimir = Nodo('console_log')
    nodoImprimir.insertHijo(Nodo('('))
    nodoImprimir.insertHijo(t[5])
    nodoImprimir.insertHijo(Nodo(')'))
    t[0] = nodoImprimir

# Declaración
def p_declaracion_inst(t):
    '''declaracion_inst : RLET ID DPUNTOS tipo IGUAL expresion
                        | RLET ID DPUNTOS tipo'''
    nodoDeclaTipo = Nodo('declaracion')
    if len(t) == 5:
        nodoDeclaTipo.insertHijo(Nodo('let'))
        nodoDeclaTipo.insertHijo(Nodo(t[2]))
        nodoDeclaTipo.insertHijo(Nodo(':'))
        nodoDeclaTipo.insertHijo(t[4])
    else:
        nodoDeclaTipo.insertHijo(Nodo('let'))
        nodoDeclaTipo.insertHijo(Nodo(t[2]))
        nodoDeclaTipo.insertHijo(Nodo(':'))
        nodoDeclaTipo.insertHijo(t[4])
        nodoDeclaTipo.insertHijo(Nodo('='))
        nodoDeclaTipo.insertHijo(t[6])
    
    t[0] = nodoDeclaTipo

def p_declaracion_array(t):
    '''declaracion_inst : RLET ID DPUNTOS tipo dimensiones_decla IGUAL expresion
                        | RLET ID DPUNTOS tipo dimensiones_decla'''
    nodoDeclaArray = Nodo('declaracion')
    if len(t) == 6:
        nodoDeclaArray.insertHijo(Nodo('let'))
        nodoDeclaArray.insertHijo(Nodo(t[2]))
        nodoDeclaArray.insertHijo(Nodo(':'))
        nodoDeclaArray.insertHijo(t[4])
        nodoDeclaArray.insertHijo(t[5])
    else:
        nodoDeclaArray.insertHijo(Nodo('let'))
        nodoDeclaArray.insertHijo(Nodo(t[2]))
        nodoDeclaArray.insertHijo(Nodo(':'))
        nodoDeclaArray.insertHijo(t[4])
        nodoDeclaArray.insertHijo(t[5])
        nodoDeclaArray.insertHijo(Nodo('='))
        nodoDeclaArray.insertHijo(t[7])
    
    t[0] = nodoDeclaArray

def p_declaracion_sin_tipo(t):
    '''declaracion_inst : RLET ID IGUAL expresion
                        | RLET ID'''
    nodoDeclaSinTipo = Nodo('declaracion')
    if len(t) == 3:
        nodoDeclaSinTipo.insertHijo(Nodo('let'))
        nodoDeclaSinTipo.insertHijo(Nodo(t[2]))
    else:
        nodoDeclaSinTipo.insertHijo(Nodo('let'))
        nodoDeclaSinTipo.insertHijo(Nodo(t[2]))
        nodoDeclaSinTipo.insertHijo(Nodo('='))
        nodoDeclaSinTipo.insertHijo(t[4])
    
    t[0] = nodoDeclaSinTipo

# Asignación
def p_asignacion_inst(t):
    'asignacion_inst : ID IGUAL expresion'
    nodoAsignacion = Nodo('asignacion')
    nodoAsignacion.insertHijo(Nodo(t[1]))
    nodoAsignacion.insertHijo(Nodo('='))
    nodoAsignacion.insertHijo(t[3])
    
    t[0] = nodoAsignacion

def p_asignacion_array(t):
    'asignacion_inst : ID dimensiones_exp IGUAL expresion'
    nodoAsigArray = Nodo('asignacion')
    nodoAsigArray.insertHijo(Nodo(t[1]))
    nodoAsigArray.insertHijo(t[2])
    nodoAsigArray.insertHijo(Nodo('='))
    nodoAsigArray.insertHijo(t[4])
    
    t[0] = nodoAsigArray

def p_dimesiones_exp(t):
    '''dimensiones_exp : dimensiones_exp CORA expresion CORC
                       | CORA expresion CORC'''
    nodoDimExp = Nodo('dimensiones')
    if len(t) == 4:
        nodoDimExp.insertHijo(Nodo('['))
        nodoDimExp.insertHijo(t[2])
        nodoDimExp.insertHijo(Nodo(']'))
    else:
        nodoDimExp.insertHijo(t[1])
        nodoDimExp.insertHijo(Nodo('['))
        nodoDimExp.insertHijo(t[3])
        nodoDimExp.insertHijo(Nodo(']'))
    t[0] = nodoDimExp

def p_dimensiones_decla(t):
    '''dimensiones_decla : dimensiones_decla CORA CORC
                         | CORA CORC'''
    nodoDimDecla = Nodo('dimensiones')
    if len(t) == 3:
        nodoDimDecla.insertHijo(Nodo('['))
        nodoDimDecla.insertHijo(Nodo(']'))
    else:
        nodoDimDecla.insertHijo(t[1])
        nodoDimDecla.insertHijo(Nodo('['))
        nodoDimDecla.insertHijo(Nodo(']'))
    t[0] = nodoDimDecla

# IF
def p_if_inst(t):
    'if_inst : RIF if_cond'
    nodoIf = Nodo('IF')
    nodoIf.insertHijo(t[2])
    t[0] = nodoIf

def p_if_cond(t):
    'if_cond : expresion LLAVEA instrucciones LLAVEC'
    nodoIfSimple = Nodo('IF')
    nodoIfSimple.insertHijo(Nodo('if'))
    nodoIfSimple.insertHijo(t[1])
    nodoIfSimple.insertHijo(Nodo('{'))
    nodoIfSimple.insertHijo(t[3])
    nodoIfSimple.insertHijo(Nodo('}'))
    
    t[0] = nodoIfSimple

def p_if_else(t):
    'if_cond : expresion LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    nodoIfElse = Nodo('IF')
    nodoIfElse.insertHijo(Nodo('if'))
    nodoIfElse.insertHijo(t[1])
    nodoIfElse.insertHijo(Nodo('{'))
    nodoIfElse.insertHijo(Nodo(t[3]))
    nodoIfElse.insertHijo(Nodo('}'))
    nodoIfElse.insertHijo(Nodo('else'))
    nodoIfElse.insertHijo(Nodo('{'))
    nodoIfElse.insertHijo(t[7])
    nodoIfElse.insertHijo(Nodo('}'))

    t[0] = nodoIfElse
    

def p_else_if(t):
    'if_cond : expresion LLAVEA instrucciones LLAVEC RELSE RIF if_cond'
    nodoElseIf = Nodo('IF')
    nodoElseIf.insertHijo(Nodo('if'))
    nodoElseIf.insertHijo(t[1])
    nodoElseIf.insertHijo(Nodo('{'))
    nodoElseIf.insertHijo(Nodo(t[3]))
    nodoElseIf.insertHijo(Nodo('}'))
    nodoElseIf.insertHijo(Nodo('else'))
    nodoElseIf.insertHijo(t[7])

    t[0] = nodoElseIf

# For
def p_for(t):
    'for_inst : RFOR PARA declaracion_inst PCOMA expresion PCOMA expresion PARC LLAVEA instrucciones LLAVEC'
    nodoFor = Nodo('FOR')
    nodoFor.insertHijo(Nodo('for'))
    nodoFor.insertHijo(Nodo('('))
    nodoFor.insertHijo(t[3])
    nodoFor.insertHijo(Nodo(';'))
    nodoFor.insertHijo(t[5])
    nodoFor.insertHijo(Nodo(';'))
    nodoFor.insertHijo(t[7])
    nodoFor.insertHijo(Nodo(')'))
    nodoFor.insertHijo(Nodo('{'))
    nodoFor.insertHijo(t[10])
    nodoFor.insertHijo(Nodo('}'))
    
    t[0] = nodoFor

# While
def p_while_inst(t):
    'while_inst : RWHILE expresion LLAVEA instrucciones LLAVEC'
    nodoWhile = Nodo('WHILE')
    nodoWhile.insertHijo(Nodo('while'))
    nodoWhile.insertHijo(t[2])
    nodoWhile.insertHijo(Nodo('{'))
    nodoWhile.insertHijo(t[4])
    nodoWhile.insertHijo(Nodo('}'))
    
    t[0] = nodoWhile

# Funciones
def p_funcion_inst(t):
    '''funcion_inst : RFUNCTION ID PARA PARC LLAVEA instrucciones LLAVEC
                    | RFUNCTION ID PARA PARC DPUNTOS tipo LLAVEA instrucciones LLAVEC'''
    nodoFunc = Nodo('funcion')
    if len(t) == 8:
        nodoFunc.insertHijo(Nodo('function'))
        nodoFunc.insertHijo(Nodo(t[2]))
        nodoFunc.insertHijo(Nodo('('))
        nodoFunc.insertHijo(Nodo(')'))
        nodoFunc.insertHijo(Nodo('{'))
        nodoFunc.insertHijo(t[6])
        nodoFunc.insertHijo(Nodo('}'))
    else:
        nodoFunc.insertHijo(Nodo('function'))
        nodoFunc.insertHijo(Nodo(t[2]))
        nodoFunc.insertHijo(Nodo('('))
        nodoFunc.insertHijo(Nodo(')'))
        nodoFunc.insertHijo(Nodo(':'))
        nodoFunc.insertHijo(t[6])
        nodoFunc.insertHijo(Nodo('{'))
        nodoFunc.insertHijo(t[8])
        nodoFunc.insertHijo(Nodo('}'))
    t[0] = nodoFunc

def p_funcion_param(t):
    '''funcion_inst : RFUNCTION ID PARA list_params PARC LLAVEA instrucciones LLAVEC
                    | RFUNCTION ID PARA list_params PARC DPUNTOS tipo LLAVEA instrucciones LLAVEC'''
    nodoFuncParam = Nodo('funcion')
    if len(t) == 9:
        nodoFuncParam.insertHijo(Nodo('function'))
        nodoFuncParam.insertHijo(Nodo(t[2]))
        nodoFuncParam.insertHijo(Nodo('('))
        nodoFuncParam.insertHijo(t[4])
        nodoFuncParam.insertHijo(Nodo(')'))
        nodoFuncParam.insertHijo(Nodo('{'))
        nodoFuncParam.insertHijo(t[7])
        nodoFuncParam.insertHijo(Nodo('}'))
    else:
        nodoFuncParam.insertHijo(Nodo('function'))
        nodoFuncParam.insertHijo(Nodo(t[2]))
        nodoFuncParam.insertHijo(Nodo('('))
        nodoFuncParam.insertHijo(t[4])
        nodoFuncParam.insertHijo(Nodo(')'))
        nodoFuncParam.insertHijo(Nodo(':'))
        nodoFuncParam.insertHijo(t[7])
        nodoFuncParam.insertHijo(Nodo('{'))
        nodoFuncParam.insertHijo(t[9])
        nodoFuncParam.insertHijo(Nodo('}'))
        
    t[0] = nodoFuncParam

def p_list_params(t):
    '''list_params : list_params COMA parametro
                   | parametro'''
    nodoListParam = Nodo('parametros')
    if len(t) != 2:
        nodoListParam.insertHijo(t[1])
        nodoListParam.insertHijo(Nodo(','))
        nodoListParam.insertHijo(t[3])
    else:
        nodoListParam.insertHijo(t[1])
    
    t[0] = nodoListParam
    
def p_parametro(t):
    '''parametro : ID DPUNTOS tipo
                 | ID'''
    nodoParam = Nodo('parametro')
    if len(t) == 2:
        nodoParam.insertHijo(Nodo(t[1]))
        nodoParam.insertHijo(Nodo(':'))
        nodoParam.insertHijo(t[3])
    else:
        nodoParam.insertHijo(Nodo(t[1]))
    
    t[0] = nodoParam

def p_parametro_array(t):
    '''parametro : ID DPUNTOS tipo dimensiones_decla'''
    nodoParamDim = Nodo('parametro')
    nodoParamDim.insertHijo(Nodo(t[1]))
    nodoParamDim.insertHijo(Nodo(':'))
    nodoParamDim.insertHijo(t[3])
    nodoParamDim.insertHijo(t[4])
    t[0] = nodoParamDim

def p_return_inst(t):
    '''return_inst : RRETURN
                   | RRETURN expresion'''
    if len(t) == 2:
        t[0] = Nodo('return')
    else:
        nodoReturn = Nodo('return')
        nodoReturn.insertHijo(t[2])
        t[0] =  nodoReturn

def p_break_inst(t):
    'break_inst : RBREAK'
    t[0] = Nodo('break')

def p_continue_inst(t):
    'continue_inst : RCONTINUE'
    t[0] = Nodo('continue')

# Expresiones
def p_expresion_aritmetica(t):
    '''expresion : expresion MAS expresion
                | expresion MENOS expresion
                | expresion POR expresion
                | expresion DIV expresion
                | expresion MOD expresion
                | expresion POT expresion
                | MENOS expresion %prec UMENOS'''
    nodoExp = Nodo('expresion')
    if len(t) == 3:
        nodoExp.insertHijo(Nodo('-'))
        nodoExp.insertHijo(t[2])
    else:
        nodoExp.insertHijo(t[1])
        nodoExp.insertHijo(Nodo(t[2]))
        nodoExp.insertHijo(t[3])
    
    t[0] = nodoExp

def p_expresion_logica(t):
    '''expresion : expresion OR expresion
                 | expresion AND expresion
                 | NOT expresion %prec UNOT'''
    
    nodoExpLogica = Nodo('expresion')
    if len(t) == 3:
        nodoExpLogica.insertHijo(Nodo('!'))
        nodoExpLogica.insertHijo(t[2])
    else:
        nodoExpLogica.insertHijo(t[1])
        nodoExpLogica.insertHijo(Nodo(t[2]))
        nodoExpLogica.insertHijo(t[3])
    
    t[0] = nodoExpLogica

def p_expresion_relacional(t):
    '''expresion : expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MAYORIGUAL expresion
                 | expresion MENORIGUAL expresion
                 | expresion DISTINTO expresion
                 | expresion IGUALIGUAL expresion'''
    
    nodoExpRel = Nodo('expresion')
    nodoExpRel.insertHijo(t[1])
    nodoExpRel.insertHijo(Nodo(t[2]))
    nodoExpRel.insertHijo(t[3])

    t[0] = nodoExpRel

def p_expresion_parentesis(t):
    'expresion : PARA expresion PARC'
    nodoExpParen = Nodo('expresion')
    nodoExpParen.insertHijo(Nodo('('))
    nodoExpParen.insertHijo(t[2])
    nodoExpParen.insertHijo(Nodo(')'))
    t[0] = nodoExpParen

def p_llamada_funcion(t):
    'llamada_func : ID PARA PARC'
    nodoLlamFunc = Nodo('llamada_funcion')
    nodoLlamFunc.insertHijo(Nodo(t[1]))
    nodoLlamFunc.insertHijo(Nodo('('))
    nodoLlamFunc.insertHijo(Nodo(')'))

    t[0] = nodoLlamFunc

def p_llamada_func_param(t):
    'llamada_func : ID PARA expresion_list PARC'
    nodoLlamFunPar = Nodo('llamada_funcion')
    nodoLlamFunPar.insertHijo(Nodo(t[1]))
    nodoLlamFunPar.insertHijo(Nodo('('))
    nodoLlamFunPar.insertHijo(t[3])
    nodoLlamFunPar.insertHijo(Nodo(')'))

    t[0] = nodoLlamFunPar

def p_llamada_array(t):
    'llamada_array : ID dimensiones_exp'
    nodoLlamArray = Nodo('llamada_array')
    nodoLlamArray.insertHijo(Nodo(t[1]))
    nodoLlamArray.insertHijo(t[2])

    t[0] = nodoLlamArray

def p_expresion_list(t):
    '''expresion_list : expresion_list COMA expresion
                      | expresion'''
    nodoExpList = Nodo('expresion_list')
    if len(t) != 2:
        nodoExpList.insertHijo(t[1])
        nodoExpList.insertHijo(Nodo(','))
        nodoExpList.insertHijo(t[3])
    else:
        nodoExpList.insertHijo(t[1])
    
    t[0] = nodoExpList

def p_expresion_primitivos(t):
    '''expresion : ENTERO
                 | DECIMAL
                 | ID
                 | CADENA
                 | RTRUE
                 | RFALSE
                 | RNULL'''
    nodoExpPrim = Nodo('expresion')
    nodoExpPrim.insertHijo(Nodo(t[1]))
    t[0] = nodoExpPrim
    
def p_expresion_incdec(t):
    '''expresion : expresion MAS MAS
                 | expresion MENOS MENOS'''
    nodoIncreDecre = Nodo('expresion')
    nodoIncreDecre.insertHijo(t[1])
    nodoIncreDecre.insertHijo(Nodo(t[2]))
    nodoIncreDecre.insertHijo(Nodo(t[3]))

    t[0] = nodoIncreDecre

def p_expresion_func(t):
    'expresion : llamada_func'
    nodoExpLlamF = Nodo('expresion')
    nodoExpLlamF.insertHijo(t[1])
    t[0] = nodoExpLlamF

def p_expresion_nativas(t):
    'expresion : nativa_exp'
    nodoExpNat = Nodo('expresion')
    nodoExpNat.insertHijo(t[1])
    t[0] = nodoExpNat

def p_expresion_arrays(t):
    'expresion : CORA expresion_list CORC'
    nodoExpArr = Nodo('expresion')
    nodoExpArr.insertHijo(Nodo('['))
    nodoExpArr.insertHijo(t[2])
    nodoExpArr.insertHijo(Nodo(']'))

    t[0] = nodoExpArr

def p_expresion_llamArra(t):
    'expresion : llamada_array'
    nodoExpArrLLam = Nodo('expresion')
    nodoExpArrLLam.insertHijo(t[1])
    t[0] = nodoExpArrLLam

def p_tipo(t):
    '''tipo : RNUMBER
            | RSTRING
            | RBOOLEAN
            | RANY'''
    nodoTipo = Nodo('tipo')
    nodoTipo.insertHijo(Nodo(str(t.slice[1].value)))

    t[0] = nodoTipo

def p_nativas(t):
    '''nativa_exp : expresion PUNTO RUPCASE PARA PARC
                  | expresion PUNTO RLOWCASE PARA PARC
                  | expresion PUNTO RTOSTRING PARA PARC
                  | RSTRINGN PARA expresion PARC
                  | expresion PUNTO RFIXED PARA expresion PARC
                  | expresion PUNTO REXPONENTIAL PARA expresion PARC
                  | RTYPEOF PARA expresion PARC
                  | RLENGTH PARA expresion PARC'''
    nodoNativa = Nodo('nativa')
    
    if len(t) == 6:
        nodoNativa.insertHijo(t[1])
        nodoNativa.insertHijo(Nodo('.'))
        nodoNativa.insertHijo(Nodo(str(t.slice[3].value)))
        nodoNativa.insertHijo(Nodo('('))
        nodoNativa.insertHijo(Nodo(')'))
    elif len(t) == 5:
        nodoNativa.insertHijo(Nodo(str(t.slice[1].value)))
        nodoNativa.insertHijo(Nodo('('))
        nodoNativa.insertHijo(t[3])
        nodoNativa.insertHijo(Nodo(')'))
    else:
        nodoNativa.insertHijo(t[1])
        nodoNativa.insertHijo(Nodo('.'))
        nodoNativa.insertHijo(Nodo(str(t.slice[3].value)))
        nodoNativa.insertHijo(Nodo('('))
        nodoNativa.insertHijo(t[5])
        nodoNativa.insertHijo(Nodo(')'))
    
    t[0] = nodoNativa

def p_error(t):
    
    if t is not None:
        print(" Error sintáctico en '%s'" % t.value)
        
#parser = yacc.yacc()

input = ''

def parseAst(inp):
    # global errores
    global parser
    # errores = []
    parser = yacc.yacc()
    global input
    input = inp
    lexer.lineno = 1
    return parser.parse(inp)
