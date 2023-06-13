
from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Simbolo import Simbolo
from Sym.Error import Error

class Declaracion(Instruccion):
    def __init__(self, ident, valor, tipo, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.valor = valor
        self.tipo = tipo

    def ejecutar(self, env):
        valorVar = self.valor

        if valorVar is not None:
            valorVar = self.valor.ejecutar(env)
        else:
            valorVar = Retorno(Tipo.NULL, None)

        # TODO: VER TIPOS NULOS

        if self.tipo == Tipo.ANY:
            valorVar.tipo = Tipo.ANY

        if self.tipo == valorVar.tipo:
            nuevoSimbolo = Simbolo(self.ident, self.tipo, valorVar.valor, self.linea, self.columna)

            if env.existeSimbEnActual(self.ident):
                return Error('Semántico', 'Variable ya está declarada', self.linea, self.columna)
            
            env.guardarVar(nuevoSimbolo)
        else:
            return Error('Semántico', 'El tipo de dato de la variable es distinto a la asignación', self.linea, self.columna)



