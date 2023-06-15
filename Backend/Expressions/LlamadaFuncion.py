from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from Instructions.Return import Return
from Sym.TablaSimbolos import TablaSimbolos
from Sym.Simbolo import Simbolo
from Sym.Error import Error

class LlamadaFuncion(Expresion):
    def __init__(self, ident, listaParams, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.listaParams = listaParams

    def ejecutar(self, env):
        # se busca la función
        funcion = env.getFuncion(self.ident)
        
        if funcion is not None:
            # creamos un nuevo entorno enviando el entorno global
            nuevoEnv = TablaSimbolos(env.getEntornoGlobal())

            # Recorremos el arreglo de parámetros
            for i, param in enumerate(self.listaParams):
                valParam = self.listaParams[i].ejecutar(env)
                if isinstance(valParam, Error): return valParam

                # Guardamos la nueva variable del parámetro
                nuevaVar = Simbolo(funcion.listParametros[i].ident, valParam.tipo, valParam.valor, self.linea, self.columna)
                nuevoEnv.guardarVar(nuevaVar)
            
            # Ejecutamos las instrucciones de la función
            for instruccion in funcion.bloqInstrucciones:
                resultado = instruccion.ejecutar(nuevoEnv)
                if isinstance(resultado, Error): return resultado

                if isinstance(resultado, Retorno):
                    if resultado.tipo == Tipo.RETURNST:
                        break
            
            return resultado