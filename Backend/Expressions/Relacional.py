
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum
from Sym.Error import Error

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
        if isinstance(opIzq, Error): return opIzq
        opDer = self.opeDer.ejecutar(env)
        if isinstance(opDer, Error): return opDer

        if opIzq.tipo == Tipo.RETURNST:
            if isinstance(opIzq.valor, int) or isinstance(opIzq.valor, float):
                opIzq.tipo = Tipo.NUMBER
            elif isinstance(opIzq.valor, str):
                opIzq.tipo = Tipo.STRING
        
        if opDer.tipo == Tipo.RETURNST:
            if isinstance(opDer.valor, int) or isinstance(opDer.valor, float):
                opDer.tipo = Tipo.NUMBER
            elif isinstance(opIzq.valor, str):
                opIzq.tipo = Tipo.STRING

        # Se inicializa el objeto Resultado con el tipo Bool por defecto
        resultado = Retorno(Tipo.BOOL, False)
        
        if self.esTipoPermitido(opIzq.tipo, opDer.tipo):
            if self.tipo == TipoRelacionales.MAYOR:
                resultado.valor = 'true' if (opIzq.valor > opDer.valor) else 'false'
            elif self.tipo == TipoRelacionales.MENOR:
                resultado.valor = 'true' if (opIzq.valor < opDer.valor) else 'false'
            elif self.tipo == TipoRelacionales.MAYORIGUAL:
                resultado.valor = 'true' if (opIzq.valor >= opDer.valor) else 'false'
            elif self.tipo == TipoRelacionales.MENORIGUAL:
                resultado.valor = 'true' if (opIzq.valor <= opDer.valor) else 'false'
            elif self.tipo == TipoRelacionales.IGUALIGUAL:
                resultado.valor = 'true' if (opIzq.valor == opDer.valor) else 'false'
            elif self.tipo == TipoRelacionales.DISTINTO:
                resultado.valor = 'true' if (opIzq.valor != opDer.valor) else 'false'
            else:
                print('Error operacion')
                return Error('Semántico', 'El tipo de operación no es permitido para operaciones relacionales', self.linea, self.columna)
        else:
            print('Error operaciones relacionales tipo')
            return Error('Semántico', 'El tipo de dato no es permitido para operaciones relacionales', self.linea, self.columna)

        return resultado
    
    def esTipoPermitido(self, tipoIzq, tipoDer):
        if (tipoIzq == Tipo.NUMBER and tipoDer == Tipo.NUMBER):
            return True
        
        if (tipoIzq == Tipo.STRING and tipoDer == Tipo.STRING):
            return True
        
        if (tipoIzq == Tipo.BOOL and tipoDer == Tipo.BOOL):
            return True
        
        if (tipoIzq == Tipo.ANY or tipoDer == Tipo.ANY):
            return True


