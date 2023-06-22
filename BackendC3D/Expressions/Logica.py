
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class TipoLogicas(Enum):
    AND = 1
    OR = 2
    NOT = 3

class Logica(Expresion):
    def __init__(self, opeIzq, opeDer, tipo, linea, columna):
        super().__init__(linea, columna)
        self.opeIzq = opeIzq
        self.opeDer = opeDer
        self.tipo = tipo

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        generador.agregarComentario('Inicio operacion logica')
        self.check_labels()
        lblAndOr = ''

        if self.tipo == TipoLogicas.AND:
            lblAndOr = generador.nuevoLbl()
            self.opeIzq.trueLbl = lblAndOr
            self.opeDer.trueLbl = self.trueLbl
            self.opeIzq.falseLbl = self.opeDer.falseLbl = self.falseLbl
        elif self.tipo == TipoLogicas.OR:
            self.opeIzq.trueLbl = self.trueLbl
            self.opeDer.trueLbl = self.trueLbl
            lblAndOr = generador.nuevoLbl()
            self.opeIzq.falseLbl(lblAndOr)
            self.opeDer.falseLbl = self.falseLbl
        elif self.tipo == TipoLogicas.NOT:
            self.opeIzq.falseLbl = self.trueLbl
            self.opeIzq.trueLbl = self.falseLbl

            opeNot = self.opeIzq.compilar(env)
            if isinstance(opeNot, Error): return opeNot

            lblTrue = opeNot.trueLbl
            lblFalse = opeNot.falseLbl
            opeNot.trueLbl = lblFalse
            opeNot.falseLbl = lblTrue
            self.tipo = Tipo.BOOL
        
            return opeNot

        # Se ejecuta el método de Primitivo, que obtiene el valor del operando
        opIzq = self.opeIzq.compilar(env)
        if isinstance(opIzq, Error): return opIzq        
        opDer = self.opeDer.compilar(env)
        if isinstance(opDer, Error): return opDer

        generador.putLbl(lblAndOr)
        generador.agregarEspacio()

        resultado = Retorno(Tipo.BOOL, None, False)
        resultado.trueLbl = self.trueLbl
        resultado.falseLbl = self.falseLbl
        generador.agregarComentario('Fin operacion logica')

        return resultado
    
    def check_labels(self):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        if self.trueLbl == '':
            self.trueLbl = generador.nuevoLbl()
        if self.falseLbl == '':
            self.falseLbl = generador.nuevoLbl()
