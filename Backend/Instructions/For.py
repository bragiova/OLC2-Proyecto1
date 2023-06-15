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
        if isinstance(varInit, Error): return varInit

        # Evaluamos la condición
        condicion = self.condicion.ejecutar(entorno)
        if isinstance(condicion, Error): return condicion

        flagBreakContinue = False

        if condicion.tipo != Tipo.BOOL:
            return Error('Semántico', 'Tipo de dato en la condición no es Boolean', self.linea, self.columna)
        
        while condicion.valor == 'true':
            # se crea un entorno por cada iteración enviando como anterior el entorno general del ciclo
            envIteracion = TablaSimbolos(entorno)
            # Se ejecuta cada instrucción del bloque
            for instruccion in self.bloqueInst:
                resultado = instruccion.ejecutar(envIteracion)

                if resultado is not None:
                    if resultado.tipo == Tipo.BREAKST or resultado.tipo == Tipo.CONTIST or resultado.tipo == Tipo.RETURNST:
                        flagBreakContinue = True
                        break
            
            if flagBreakContinue:
                if resultado.tipo == Tipo.BREAKST:
                    break
                elif resultado.tipo == Tipo.RETURNST:
                    return resultado

            # Actualizamos el valor de la variable inicial según el rango (incremento-decremento)
            initActualizado = self.expreRango.ejecutar(entorno)
            if isinstance(initActualizado, Error): return initActualizado

            # Se crea un nuevo símbolo con el valor actualizado de la variable inicial
            nuevoSimbolo = Simbolo(self.varInicio.ident, self.varInicio.tipo, initActualizado.valor, self.linea, self.columna)
            # Actualizamos al tabla de símbolos
            actualValor = entorno.updateTabla(nuevoSimbolo)
            # Se evalúa nuevamente la condición tomando en cuenta el nuevo valor de la variable inicial
            condicion = self.condicion.ejecutar(entorno)
            if isinstance(condicion, Error): return condicion

            if condicion.tipo != Tipo.BOOL:
                return Error('Semántico', 'Tipo de dato en la condición no es Boolean', self.linea, self.columna)
        return None
