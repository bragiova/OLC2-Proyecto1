import os
from flask import Flask, request
import json
from flask_cors import CORS
from werkzeug.utils import redirect
from flask.helpers import url_for

import Sintactico as Analizar
from Sym.TablaSimbolos import *
from Sym.Error import Error
from Instructions.ImprimirClg import ImprimirClg
from Abstract.Retorno import Tipo
from Sym.GeneradorC3D import GeneradorC3D

app = Flask(__name__)
CORS(app)

def compilar(txtEntrada):
    genAux = GeneradorC3D()
    genAux.limpiarTodo()
    generador = genAux.getInstancia()
    C3D = ''

    env = TablaSimbolos()
    try:
        ast = Analizar.parse(txtEntrada)
        TablaSimbolos.entrada = txtEntrada
        TablaSimbolos.variables = {}
        TablaSimbolos.funciones = {}
        TablaSimbolos.errores = []
        for inst in ast:
            instRet = inst.compilar(env)
            if isinstance(instRet, Error): TablaSimbolos.errores.append(instRet)
        
        C3D = generador.getCodigo()
    except Exception as err:
        print('error except: ', err)
        ImprimirClg.salidaConsola = 'Error de compilación'
    return C3D

@app.route('/entradaC3D', methods = ['GET', 'POST'])
def entrada():
    if request.method == 'POST':
        data = request.get_json(force=True)
        codigo = compilar(data['codigo'])
        ImprimirClg.salidaConsola = ''
        return {'c3d': codigo}

@app.route('/simbolosC3D', methods = ['GET'])
def repSimbolos():
    objTablaSimb = {}
    listSimbolos = []

    for simbKey in TablaSimbolos.variables.keys():
        objSimb = {}
        objSimb['id'] = simbKey
        objSimb['tipo'] = getTipo(TablaSimbolos.variables[simbKey].getTipo())
        objSimb['linea'] = str(TablaSimbolos.variables[simbKey].getLinea())
        objSimb['colum'] = str(TablaSimbolos.variables[simbKey].getColumna())
        listSimbolos.append(objSimb)
    
    for funKey in TablaSimbolos.funciones.keys():
        objFunc = {}
        objFunc['id'] = funKey
        objFunc['tipo'] = 'Función'
        objFunc['linea'] = str(TablaSimbolos.funciones[funKey].linea)
        objFunc['colum'] = str(TablaSimbolos.funciones[funKey].columna)
        listSimbolos.append(objFunc)
    
    objTablaSimb['simbolos'] = listSimbolos
    return objTablaSimb

@app.route('/erroresC3D', methods = ['GET'])
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

def getTipo(tipo):
    if tipo == Tipo.NUMBER:
        return 'number'
    elif tipo == Tipo.STRING:
        return 'string'
    elif tipo == Tipo.BOOL:
        return 'boolean'
    elif tipo == Tipo.ANY:
        return 'any'
    else:
        return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port=3001)

# def pruebaError():
#     for err in TablaSimbolos.errores:
#         print(err.tipoError, err.desc, err.linea, err.columna)

# def pruebaSimb():
#     for simb in TablaSimbolos.variables.keys():
#         print(TablaSimbolos.variables[simb].getId(), TablaSimbolos.variables[simb].getTipo(), TablaSimbolos.variables[simb].getLinea())

# def main():
#     env = TablaSimbolos()
    
#     absolutepath = os.path.abspath(__file__)
#     fileDirectory = os.path.dirname(absolutepath)
#     # print(os.path.join(fileDirectory, 'archivosPruebas', 'archivoPrueba.txt'))
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'archivoPrueba.ts'), 'r')

#     f = open(os.path.join(fileDirectory, 'archivosPruebas', 'entrada_facilita.ts'), 'r')
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'funcionesbasicas.ts'), 'r')
#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'funcionesrecursivas.ts'), 'r')

#     # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'entrada_intermedia.ts'), 'r')
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
#     genAux = GeneradorC3D()
#     genAux.limpiarTodo()
#     generador = genAux.getInstancia()

#     ast = Analizar.parse(s)

#     for inst in ast:
#         valRet = inst.compilar(env)
#         if isinstance(valRet, Error): TablaSimbolos.errores.append(valRet)

#     C3D = generador.getCodigo()
#     fi = open('salida.go', 'w')
#     fi.write(C3D)
#     fi.close()
#     # pruebaError()
#     pruebaSimb()
#     # print(ImprimirClg.salidaConsola)

# main()