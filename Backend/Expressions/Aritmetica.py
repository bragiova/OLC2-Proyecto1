import math
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum
from Sym.Error import Error

class TipoOperacionAritmetica(Enum):
    SUMA = 1
    RESTA = 2
    MULTI = 3
    DIV = 4
    MOD = 5
    POT = 6

class Aritmetica(Expresion):
    def __init__(self, opeIzq, opeDer, operacion, linea, columna):
        self.opIzq = opeIzq
        self.opDer = opeDer
        self.operacion = operacion
        super().__init__(linea, columna)

    def ejecutar(self, env):
        # Se ejecuta el método de Primitivo, que obtiene el valor del operando
        opIzq = self.opIzq.ejecutar(env)
        if isinstance(opIzq, Error): return opIzq
        opDer = self.opDer.ejecutar(env)
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

        # Se inicializa el objeto Resultado con el tipo Number por defecto
        resultado = Retorno(Tipo.NUMBER, 0)
        esPermitido = self.esTipoPermitido(opIzq.tipo, opDer.tipo)

        if self.operacion == TipoOperacionAritmetica.SUMA:
            if esPermitido or (opIzq.tipo == Tipo.STRING and opDer.tipo == Tipo.STRING):
                resultado.valor = opIzq.valor + opDer.valor
                # Se cambia tipo del resultado si son string operandos, operador ternario
                resultado.tipo = (Tipo.STRING if (opIzq.tipo == Tipo.STRING and opDer.tipo == Tipo.STRING) else resultado.tipo)
            else:
                print('Error en tipo de dato - suma')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación suma', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.RESTA:
            if esPermitido:
                resultado.valor = opIzq.valor - opDer.valor
            else:
                print('Error en tipo de dato - resta')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación resta', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.MULTI:
            if esPermitido:
                resultado.valor = opIzq.valor * opDer.valor
            else:
                print('Error en tipo de dato - multiplicación')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación multiplicación', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.DIV:
            if esPermitido:
                if opDer.valor > 0:
                    resultado.valor = opIzq.valor / opDer.valor
                else:
                    return Error('Semántico', 'No se puede realizar una división entre 0', self.linea, self.columna)
            else:
                print('Error en tipo de dato - división')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación división', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.MOD:
            if esPermitido:
                if opDer.valor > 0:
                    # resultado.valor = opIzq.valor % opDer.valor
                    resultado.valor = math.fmod(opIzq.valor, opDer.valor)
                else:
                    return Error('Semántico', 'No se puede realizar la operación módulo entre 0', self.linea, self.columna)
            else:
                print('Error en tipo de dato - módulo')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación módulo', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.POT:
            if esPermitido:
                resultado.valor = opIzq.valor ** opDer.valor
            else:
                print('Error en tipo de dato - potencia')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación potencia', self.linea, self.columna)
        else:
            print('Error operacion')
            return Error('Semántico', 'El tipo de operación no es permitido para operaciones aritméticas', self.linea, self.columna)
        
        return resultado
    
    def esTipoPermitido(self, tipoIzq, tipoDer):
        if (tipoIzq == Tipo.NUMBER and tipoDer == Tipo.NUMBER):
            return True
        
        if (tipoIzq == Tipo.STRING and tipoDer == Tipo.STRING):
            return True
        
        if (tipoIzq == Tipo.ANY or tipoDer == Tipo.ANY):
            return True
