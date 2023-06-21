from Abstract.Instruccion import Instruccion

class Funcion(Instruccion):
    def __init__(self, ident, listParametros, bloqInstrucciones, tipoFuncion, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.listParametros = listParametros
        self.bloqInstrucciones = bloqInstrucciones
        self.tipoFuncion = tipoFuncion

    def ejecutar(self, env):
        env.guardarFuncion(self.ident, self)
