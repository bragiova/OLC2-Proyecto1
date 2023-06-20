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

# app = Flask(__name__)
# CORS(app)

# def interpretar(entrada):
#     env = TablaSimbolos()
#     ast = Analizar.parse(entrada)
#     for inst in ast:
#         inst.ejecutar(env)
#     return {'msg': 'interpretar'}

# @app.route('/prueba', methods = ['POST'])
# def prueba():
#     data = request.get_json(force=True)
#     codigo = interpretar(data['code'])
#     return {'txt': codigo}

# if __name__ == '__main__':
#     app.run(debug = True, port=3000)

def pruebaError():
    for err in TablaSimbolos.errores:
        print(err.tipoError, err.desc, err.linea, err.columna)

def main():
    env = TablaSimbolos()
    
    absolutepath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(absolutepath)
    # print(os.path.join(fileDirectory, 'archivosPruebas', 'archivoPrueba.txt'))
    # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'archivoPrueba.txt'), 'r')
    f = open(os.path.join(fileDirectory, 'archivosPruebas', 'entrada_facilita.ts'), 'r')
    # f = open(os.path.join(fileDirectory, 'archivosPruebas', 'entrada_intermedia.ts'), 'r')
    s = f.read()
    # s = '''
    #     // prueba comentario
    #     /* comentario
    #     multilinea
    #     */
    #     let a:string = "hola";
    #     let b = 50+10*5;
    #     let c:string = "mundo";
    #     console.log(a);
    #     console.log(b);
    #     console.log(a + c);
    #     '''
    ast = Analizar.parse(s)

    for inst in ast:
        valRet = inst.ejecutar(env)
        if isinstance(valRet, Error): TablaSimbolos.errores.append(valRet)

    pruebaError()
    # print(ImprimirClg.salidaConsola)

main()