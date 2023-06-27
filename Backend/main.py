import os
import sys
from flask import Flask, request
import json
from flask_cors import CORS
from werkzeug.utils import redirect
from flask.helpers import url_for
import graphviz
import base64

import Sintactico as Analizar
from Sym.TablaSimbolos import *
from Sym.Error import Error
from Instructions.ImprimirClg import ImprimirClg
from Abstract.Retorno import Tipo
import gramaticaAST as ArbolAST

sys.setrecursionlimit(3000)

app = Flask(__name__)
CORS(app)

def interpretar(txtEntrada):
    env = TablaSimbolos()
    try:
        ast = Analizar.parse(txtEntrada)
        TablaSimbolos.entrada = txtEntrada
        TablaSimbolos.variables = {}
        TablaSimbolos.funciones = {}
        TablaSimbolos.errores = []
        for inst in ast:
            instRet = inst.ejecutar(env)
            if isinstance(instRet, Error): TablaSimbolos.errores.append(instRet)
    except Exception as err:
        print('error except: ', err)
        ImprimirClg.salidaConsola += 'Ocurrieron errores al interpretar'
    return ImprimirClg.salidaConsola

@app.route('/entrada', methods = ['GET', 'POST'])
def entrada():
    if request.method == 'POST':
        data = request.get_json(force=True)
        codigo = interpretar(data['codigo'])
        ImprimirClg.salidaConsola = ''
        return {'consola': codigo}

@app.route('/simbolos', methods = ['GET'])
def repSimbolos():
    objTablaSimb = {}
    listSimbolos = []

    for simbKey in TablaSimbolos.variables.keys():
        objSimb = {}
        objSimb['id'] = simbKey
        objSimb['tipo'] = getTipo(TablaSimbolos.variables[simbKey].getTipo())
        objSimb['valor'] = str(TablaSimbolos.variables[simbKey].getValor())
        objSimb['linea'] = str(TablaSimbolos.variables[simbKey].getLinea())
        objSimb['colum'] = str(TablaSimbolos.variables[simbKey].getColumna())
        listSimbolos.append(objSimb)
    
    for funKey in TablaSimbolos.funciones.keys():
        objFunc = {}
        objFunc['id'] = funKey
        objFunc['tipo'] = 'Función'
        objFunc['valor'] = 'instrucción'
        objFunc['linea'] = str(TablaSimbolos.funciones[funKey].linea)
        objFunc['colum'] = str(TablaSimbolos.funciones[funKey].columna)
        listSimbolos.append(objFunc)
    
    objTablaSimb['simbolos'] = listSimbolos
    return objTablaSimb

@app.route('/errores', methods = ['GET'])
def repErrores():
    listErrores = []
    objErrores = {}

    for simError in TablaSimbolos.errores:
        objError = {}
        objError['tipo'] = simError.tipoError
        objError['desc'] = simError.desc
        objError['fila'] = simError.linea
        objError['colum'] = simError.columna
        listErrores.append(objError)
    
    objErrores['errores'] = listErrores
    return objErrores

@app.route('/ast', methods = ['GET'])
def repAST():
    objAST = {}
    grafo = graphviz.Digraph('AST', comment='prueba ast')
    try:
        salidaDot = ArbolAST.parseAst(TablaSimbolos.entrada)
        grafo.body = salidaDot

        output = grafo.pipe(format='svg')
        output1 = base64.b64encode(output).decode('utf-8')

        objAST['ast'] = output1
    except Exception as err:
        print('error except: ', err)
        
    return objAST

def getTipo(tipo):
    if tipo == Tipo.NUMBER:
        return 'number'
    elif tipo == Tipo.STRING:
        return 'string'
    elif tipo == Tipo.BOOL:
        return 'boolean'
    elif tipo == Tipo.ANY:
        return 'any'
    elif tipo == Tipo.ARREGLO:
        return 'arreglo'
    else:
        return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port=3000)

# def pruebaError():
#     for err in TablaSimbolos.errores:
#         print(err.tipoError, err.desc, err.linea, err.columna)

# def pruebaSimb():
#     for simb in TablaSimbolos.variables.keys():
#         print(TablaSimbolos.variables[simb].getId(), TablaSimbolos.variables[simb].getValor())

# def main():
#     env = TablaSimbolos()
    
#     absolutepath = os.path.abspath(__file__)
#     fileDirectory = os.path.dirname(absolutepath)
#     # print(os.path.join(fileDirectory, 'archivosPruebas', 'archivoPrueba.txt'))
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'archivoPrueba.ts'), 'r')
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'entrada_facilita.ts'), 'r')
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'entrada_intermedia.ts'), 'r')
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'funcionesbasicas1.ts'), 'r')
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'funcionesrecursivas1.ts'), 'r')
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'arreglos1d.ts'), 'r')
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'arreglos2d.ts'), 'r')
#     s = f.read()
#     # s = '''
#     #     // prueba comentario
#     #     /* comentario
#     #     multilinea
#     #     */
#     #     let a:string = "hola";
#     #     let b = 50+10*5;
#     #     let c:string = "mundo";
#     #     console.log(a);
#     #     console.log(b);
#     #     console.log(a + c);
#     #     '''
#     # ast = Analizar.parse(s)

#     # for inst in ast:
#     #     valRet = inst.ejecutar(env)
#     #     if isinstance(valRet, Error): TablaSimbolos.errores.append(valRet)

#     # pruebaError()
#     # pruebaSimb()
#     # print(ImprimirClg.salidaConsola)

#     prueba = graphviz.Digraph(comment='prueba ast')

#     salidaDot = ArbolAST.parseAst(s)
#     prueba.body = salidaDot

#     output = prueba.pipe(format='png')
#     output1 = base64.b64encode(output).decode('utf-8')
#     print(salidaDot)

# main()