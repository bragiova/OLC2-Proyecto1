from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from Sym.GeneradorC3D import GeneradorC3D

class Primitivo(Expresion):
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        super().__init__(linea, columna)

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()

        if self.tipo == Tipo.NUMBER:
            return Retorno(self.tipo, str(self.valor), False)
        elif self.tipo == Tipo.STRING:
            retTemp = generador.agregarTemp()
            generador.agregarAsig(retTemp, 'H')
            # generador.agregarExp(retTemp, 'H', '', '')
            # generador.setHeap('H', 0)
            # generador.nextHeap()

            for char in str(self.valor):
                generador.setHeap('H', ord(char))
                generador.nextHeap()
            
            generador.setHeap('H', '-1')
            generador.nextHeap()

            return Retorno(Tipo.STRING, retTemp, True)
        elif self.tipo == Tipo.BOOL:
            self.verificarLbl()

            if self.valor:
                generador.agregarGoTo(self.trueLbl)
                generador.agregarComentario('GOTO para evitar error')
                generador.agregarGoTo(self.falseLbl)
            else:
                generador.agregarGoTo(self.falseLbl)
                generador.agregarComentario('GOTO para evitar error')
                generador.agregarGoTo(self.trueLbl)
            
            ret = Retorno(self.tipo, self.valor, False)
            ret.trueLbl = self.trueLbl
            ret.falseLbl = self.falseLbl

            return ret

        # return Retorno(self.tipo, self.valor)
    
    def verificarLbl(self):
        genAux2 = GeneradorC3D()
        generador2 = genAux2.getInstancia()

        # atributos heredados de Instruccion
        if self.trueLbl == '':
            self.trueLbl = generador2.nuevoLbl()

        if self.falseLbl == '':
            self.falseLbl = generador2.nuevoLbl()
