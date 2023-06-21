from enum import Enum

class Tipo(Enum):
    NULL = 0
    NUMBER = 1
    BOOL = 2
    STRING = 3
    ANY = 4
    ARREGLO = 5
    INTERFAZ = 6

    RETURNST = 7
    CONTIST = 8
    BREAKST = 9

class Retorno:
    def __init__(self, tipo, valor, esTemp, tipoAux = ''):
        self.tipo = tipo
        self.valor = valor
        self.esTemp = esTemp
        self.tipoAux = tipoAux
        self.trueLbl = ''
        self.falseLbl = ''
