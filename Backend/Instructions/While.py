from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.TablaSimbolos import TablaSimbolos
from Sym.Simbolo import Simbolo
from Sym.Error import Error

class While(Instruccion):
    def __init__(self, condicion, bloqInstrucciones, linea, columna):
        super().__init__(linea, columna)
        self.condicion = condicion
        self.bloqInstrucciones = bloqInstrucciones

    def ejecutar(self, env):
        condicion = self.condicion.ejecutar(env)
        entorno = TablaSimbolos(env)

        if condicion.tipo != Tipo.BOOL:
            return Error('Semántico', 'Tipo de dato en la condición no es Boolean', self.linea, self.columna)
        
        while condicion.valor:
            for instruccion in self.bloqInstrucciones:
                resultado = instruccion.ejecutar(entorno)

            condicion = self.condicion.ejecutar(env)

            if condicion.tipo != Tipo.BOOL:
                return Error('Semántico', 'Tipo de dato en la condición no es Boolean', self.linea, self.columna)
            
        return None


