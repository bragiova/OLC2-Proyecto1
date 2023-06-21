
from abc import ABC, abstractmethod

class Expresion(ABC):
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna
        self.trueLbl = ''
        self.falseLbl = ''

    @abstractmethod
    def compilar(self, env): pass
