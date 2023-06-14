
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum


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
        opDer = self.opDer.ejecutar(env)
        
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
        esNumber = (opIzq.tipo == Tipo.NUMBER and opDer.tipo == Tipo.NUMBER)

        if self.operacion == TipoOperacionAritmetica.SUMA:
            if esNumber or (opIzq.tipo == Tipo.STRING and opDer.tipo == Tipo.STRING):
                resultado.valor = opIzq.valor + opDer.valor
                # Se cambia tipo del resultado si son string operandos, operador ternario
                resultado.tipo = (Tipo.STRING if (opIzq.tipo == Tipo.STRING and opDer.tipo == Tipo.STRING) else resultado.tipo)
            else:
                print('Error en tipo de dato - suma')
                resultado.valor = ''
        elif self.operacion == TipoOperacionAritmetica.RESTA:
            if esNumber:
                resultado.valor = opIzq.valor - opDer.valor
            else:
                print('Error en tipo de dato - resta')
                resultado.valor = ''
        elif self.operacion == TipoOperacionAritmetica.MULTI:
            if esNumber:
                resultado.valor = opIzq.valor * opDer.valor
            else:
                print('Error en tipo de dato - multiplicación')
                resultado.valor = ''
        elif self.operacion == TipoOperacionAritmetica.DIV:
            if esNumber:
                resultado.valor = opIzq.valor / opDer.valor
            else:
                print('Error en tipo de dato - división')
                resultado.valor = ''
        elif self.operacion == TipoOperacionAritmetica.MOD:
            if esNumber:
                resultado.valor = opIzq.valor % opDer.valor
            else:
                print('Error en tipo de dato - módulo')
                resultado.valor = ''
        elif self.operacion == TipoOperacionAritmetica.POT:
            if esNumber:
                resultado.valor = opIzq.valor ** opDer.valor
            else:
                print('Error en tipo de dato - potencia')
                resultado.valor = ''
        else:
            print('Error operacion')
            resultado.valor = ''
        
        return resultado
