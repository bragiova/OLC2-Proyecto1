from enum import Enum

class Tipo(Enum):
    NULL = 0
    NUMBER = 1
    BOOL = 2
    STRING = 3
    ARREGLO = 4
    INTERFAZ = 5

    RETURNST = 6
    CONTIST = 7
    BREAKST = 8

class Retorno:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
