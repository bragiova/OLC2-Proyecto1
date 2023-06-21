
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum
from Sym.Error import Error

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
        if isinstance(opIzq, Error): return opIzq
        opDer = self.opeDer.ejecutar(env)
        if isinstance(opDer, Error): return opDer

        # Se inicializa el objeto Resultado con el tipo Bool por defecto
        resultado = Retorno(Tipo.BOOL, 0)
        esBoolean = (opIzq.tipo == Tipo.BOOL and opDer.tipo == Tipo.BOOL)

        # Se realiza una "traducción" temporal para realizar la comparación lógica
        opIzq.valor = self.convertirBool(opIzq.valor)
        opDer.valor = self.convertirBool(opDer.valor)

        if esBoolean:
            if self.tipo == TipoLogicas.AND:
                resultado.valor = 'true' if (opIzq.valor and opDer.valor) else 'false'
            elif self.tipo == TipoLogicas.OR:
                resultado.valor = 'true' if (opIzq.valor or opDer.valor) else 'false'
            elif self.tipo == TipoLogicas.NOT:
                # Solamente se niega el valor inzquierdo, ya que se manda tanto en izq como en der desde la gramática
                resultado.valor = 'true' if (opIzq.valor == False) else 'false'
            else:
                print('Error operacion')
                resultado.valor = ''
        else:
            print('Error operaciónes lógicas tipo')
            resultado.valor = ''

        return resultado
    
    def convertirBool(self, valorOp):
        if valorOp == 'true':
            return True
        elif valorOp == 'false':
            return False
        else:
            return valorOp
