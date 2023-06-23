from Abstract.Instruccion import Instruccion

class ParametroFuncion(Instruccion):
    def __init__(self, ident, tipo, linea, columna, esArray = False):
        super().__init__(linea, columna)
        self.ident = ident
        self.tipo = tipo
        self.esArray = esArray

    def ejecutar(self, env):
        return self
