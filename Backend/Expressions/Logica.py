
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum

class TipoLogicas(Enum):
    AND = 1
    OR = 2
    NOT = 3

class Logica(Expresion):
    def __init__(self, opeIzq, opeDer, tipo, linea, columna):
        super().__init__(linea, columna)
        self.opeIzq = opeIzq
        self.opeDer = opeDer
        self.tipo = tipo

    def ejecutar(self, env):
        # Se ejecuta el método de Primitivo, que obtiene el valor del operando
        opIzq = self.opeIzq.ejecutar(env)
        opDer = self.opeDer.ejecutar(env)

        # Se inicializa el objeto Resultado con el tipo Bool por defecto
        resultado = Retorno(Tipo.BOOL, 0)
        esBoolean = (opIzq.tipo == Tipo.BOOL and opDer.tipo == Tipo.BOOL)

        if esBoolean:
            if self.tipo == TipoLogicas.AND:
                resultado.valor = opIzq.valor and opDer.valor
            elif self.tipo == TipoLogicas.OR:
                resultado.valor = opIzq.valor or opDer.valor
            elif self.tipo == TipoLogicas.NOT:
                # Solamente se niega el valor inzquierdo, ya que se manda tanto en izq como en der desde la gramática
                resultado.valor = not opIzq.valor
            else:
                print('Error operacion')
                resultado.valor = ''
        else:
            print('Error operaciónes lógicas tipo')
            resultado.valor = ''

        return resultado
