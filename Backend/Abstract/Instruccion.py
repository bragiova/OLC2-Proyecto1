
from abc import ABC, abstractmethod

class Instruccion(ABC):
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    @abstractmethod
    def ejecutar(self, env): pass
