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

        # TODO: FALTA VERIFICAR TIPOS
        if simbVar is not None:
            valVariable = self.valor.ejecutar(env)
            simbActualizado = Simbolo(simbVar.getId(), simbVar.getTipo(), valVariable.valor, self.linea, self.columna)
            env.updateTabla(simbActualizado)
        else:
            return Error('Semántico', 'Variable no existe', self.linea, self.columna)
