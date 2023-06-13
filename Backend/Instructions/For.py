from Abstract.Instruccion import Instruccion
from Sym.TablaSimbolos import TablaSimbolos
from Abstract.Retorno import *
from Sym.Error import Error
from Sym.Simbolo import Simbolo

class For(Instruccion):
    def __init__(self, varInicio, condicion, expreRango, bloqueInst, linea, columna):
        super().__init__(linea, columna)
        self.varInicio = varInicio
        self.condicion = condicion
        self.expreRango = expreRango
        self.bloqueInst = bloqueInst

    def ejecutar(self, env):
        entorno = TablaSimbolos(env)
        # Se almacena en la TS la variable inicial del ciclo
        varInit = self.varInicio.ejecutar(entorno)
        # Evaluamos la condición
        condicion = self.condicion.ejecutar(entorno)

        if condicion.tipo != Tipo.BOOL:
            return Error('Semántico', 'Tipo de dato en la condición no es Boolean', self.linea, self.columna)
        
        while condicion.valor:
            # Se ejecuta cada instrucción del bloque
            for instruccion in self.bloqueInst:
                resultado = instruccion.ejecutar(entorno)

            # Actualizamos el valor de la variable inicial según el rango (incremento-decremento)
            initActualizado = self.expreRango.ejecutar(entorno)
            # Se crea un nuevo símbolo con el valor actualizado de la variable inicial
            nuevoSimbolo = Simbolo(self.varInicio.ident, self.varInicio.tipo, initActualizado.valor, self.linea, self.columna)
            # Actualizamos al tabla de símbolos
            actualValor = entorno.updateTabla(nuevoSimbolo)
            # Se evalúa nuevamente la condición tomando en cuenta el nuevo valor de la variable inicial
            condicion = self.condicion.ejecutar(entorno)

            if condicion.tipo != Tipo.BOOL:
                return Error('Semántico', 'Tipo de dato en la condición no es Boolean', self.linea, self.columna)
        return None
