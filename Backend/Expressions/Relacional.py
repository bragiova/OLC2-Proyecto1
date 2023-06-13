
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum

class TipoRelacionales(Enum):
    MAYOR = 1
    MENOR = 2
    MAYORIGUAL = 3
    MENORIGUAL = 4
    IGUALIGUAL = 5
    DISTINTO = 6

class Relacional(Expresion):
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
        resultado = Retorno(Tipo.BOOL, False)
        esTipoPermitido = (opIzq.tipo == Tipo.NUMBER and opDer.tipo == Tipo.NUMBER) or (opIzq.tipo == Tipo.STRING and opDer.tipo == Tipo.STRING)
        
        if esTipoPermitido:
            if self.tipo == TipoRelacionales.MAYOR:
                resultado.valor = opIzq.valor > opDer.valor
            elif self.tipo == TipoRelacionales.MENOR:
                resultado.valor = opIzq.valor < opDer.valor
            elif self.tipo == TipoRelacionales.MAYORIGUAL:
                resultado.valor = opIzq.valor >= opDer.valor
            elif self.tipo == TipoRelacionales.MENORIGUAL:
                resultado.valor = opIzq.valor <= opDer.valor
            elif self.tipo == TipoRelacionales.IGUALIGUAL:
                resultado.valor = opIzq.valor == opDer.valor
            elif self.tipo == TipoRelacionales.DISTINTO:
                resultado.valor = opIzq.valor != opDer.valor
            else:
                print('Error operacion')
                resultado.valor = ''
        else:
            print('Error operaciones relacionales tipo')
            resultado.valor = ''

        return resultado


