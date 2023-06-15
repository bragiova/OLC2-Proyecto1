from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Simbolo import Simbolo
from Sym.Error import Error

class Asignacion(Instruccion):
    def __init__(self, ident, valor, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.valor = valor

    def ejecutar(self, env):
        simbVar = env.getSimbolo(self.ident)

        if simbVar is not None:
            valVariable = self.valor.ejecutar(env)
            if isinstance(valVariable, Error): return valVariable

            if (simbVar.getTipo() != valVariable.tipo) and simbVar.getTipo() != Tipo.ANY:
                print('Error', 'El valor a asignar no es del mismo tipo que la variable')
                return Error('Semántico', 'El valor a asignar no es del mismo tipo que la variable', self.linea, self.columna)

            simbActualizado = Simbolo(simbVar.getId(), simbVar.getTipo(), valVariable.valor, self.linea, self.columna)
            env.updateTabla(simbActualizado)
        else:
            return Error('Semántico', 'Variable no existe', self.linea, self.columna)
