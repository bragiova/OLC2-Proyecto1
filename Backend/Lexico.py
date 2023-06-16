
import ply.lex as lex
import sys

errores = []

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
    t.lexer.lineno += t.value.count("\n")

#Error
def t_error(t):
    #errores.append(Excepcion("Lexico", "Error Lexico" + t.value[0], t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

def find_column(inp, tk):
    line_start = inp.rfind('\n', 0, tk.lexpos) + 1
    return (tk.lexpos - line_start) + 1

lexer = lex.lex()
