
from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class ImprimirClg(Instruccion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        super().__init__(linea, columna)

    def ejecutar(self, env):
        txtImprimir = ''
        for expre in self.expresion:
            expreVal = expre.ejecutar(env)
            if isinstance(expreVal, Error): return expreVal
            
            txtImprimir += str(expreVal.valor) + ' '
        
        print(txtImprimir)
        return Retorno(Tipo.STRING, txtImprimir)