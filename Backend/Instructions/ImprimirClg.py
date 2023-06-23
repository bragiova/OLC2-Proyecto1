
from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class ImprimirClg(Instruccion):
    salidaConsola = ''

    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        super().__init__(linea, columna)

    def ejecutar(self, env):
        txtImprimir = ''
        for expre in self.expresion:
            expreVal = expre.ejecutar(env)
            if isinstance(expreVal, Error): return expreVal
            
            if isinstance(expreVal.valor, list):
                txtImprimir += '['
                strArray = self.imprimirArray(expreVal.valor)
                txtImprimir += strArray + ']'
            else:
                txtImprimir += str(expreVal.valor) + ' '
        
        print(txtImprimir)
        # Se crea una variable global para ir concatenando todo lo que debe imprimirse en consola
        ImprimirClg.salidaConsola += txtImprimir + '\n'
        return Retorno(Tipo.STRING, txtImprimir)
    
    def imprimirArray(self, listValores):
        strSalida = ''

        for i, item in enumerate(listValores):
            if isinstance(item, list):
                strSalida += '[' + self.imprimirArray(item) + ']'
            else:
                strSalida += str(item.valor)

            if i < len(listValores) - 1:
                strSalida += ','

        return strSalida