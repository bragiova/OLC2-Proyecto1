
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class TipoRelacionales(Enum):
    MAYOR = 1
    MENOR = 2
    MAYORIGUAL = 3
    MENORIGUAL = 4
    IGUALIGUAL = 5
    DISTINTO = 6

class Relacional(Expresion):
    def __init__(self, opeIzq, opeDer, tipo, linea, columna):
        super().__init__(linea, columna)
        self.opeIzq = opeIzq
        self.opeDer = opeDer
        self.tipo = tipo
    
    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()

        generador.agregarComentario('Inicio expresión relacional')
        # Se ejecuta el método de Primitivo, que obtiene el valor del operando
        opIzq = self.opeIzq.compilar(env)
        if isinstance(opIzq, Error): return opIzq
        
        opDer = None
        resultado = Retorno(Tipo.BOOL, None, False)

        if opIzq.tipo != Tipo.BOOL:
            opDer = self.opeDer.compilar(env)
            if isinstance(opDer, Error): return opDer

            if self.esTipoPermitido(opIzq.tipo, opDer.tipo):
                if opIzq.tipo == Tipo.NUMBER and opDer.tipo == Tipo.NUMBER:
                    self.check_labels()
                    generador.agregarIf(opIzq.valor, opDer.valor, self.getTipoOperacion(), self.trueLbl)
                    generador.agregarGoTo(self.falseLbl)
                elif opIzq.tipo == Tipo.STRING and opDer.tipo == Tipo.STRING:
                    inicioLbl = generador.nuevoLbl()
                    punt1 = generador.agregarTemp()
                    punt2 = generador.agregarTemp()
                    val1 = generador.agregarTemp()
                    val2 = generador.agregarTemp()
                    self.check_labels()

                    generador.agregarExp(punt1, opIzq.valor, '', '')
                    generador.agregarExp(punt2, opDer.valor, '', '')
                    generador.putLbl(inicioLbl)
                    generador.agregarIf(val1, '-1', '==', self.trueLbl)
                    generador.getHeap(val1, punt1)
                    generador.getHeap(val2, punt2)
                    generador.agregarExp(punt1, punt1, '1', '+')
                    generador.agregarExp(punt2, punt2, '1', '+')
                    generador.agregarIf(val1, val2, '==', inicioLbl)
                    generador.agregarIf(val1, val2, '!=', self.falseLbl)
                    generador.agregarGoTo(self.falseLbl)
        else:
            goToDer = generador.nuevoLbl()
            izqTemp = generador.agregarTemp()
            generador.putLbl(opIzq.trueLbl)
            generador.agregarExp(izqTemp, '1', '', '')
            generador.agregarGoTo(goToDer)
            generador.putLbl(opIzq.falseLbl)
            generador.agregarExp(izqTemp, '0', '', '')
            generador.putLbl(goToDer)

            opDer = self.opeDer.compilar(env)
            if isinstance(opDer, Error): return opDer

            goToFin = generador.nuevoLbl()
            derTemp = generador.agregarTemp()
            generador.putLbl(opDer.trueLbl)
            generador.agregarExp(derTemp, '1', '', '')
            generador.agregarGoTo(goToFin)
            generador.putLbl(opDer.falseLbl)
            generador.agregarExp(derTemp, '0', '', '')
            generador.putLbl(goToFin)

            self.check_labels()
            generador.agregarIf(izqTemp, derTemp, self.getTipoOperacion(), self.trueLbl)
            generador.agregarGoTo(self.falseLbl)
        
        generador.agregarComentario('Fin expresión relacional')
        generador.agregarEspacio()
        resultado.trueLbl = self.trueLbl
        resultado.falseLbl = self.falseLbl

        return resultado
    
    def esTipoPermitido(self, tipoIzq, tipoDer):
        if (tipoIzq == Tipo.NUMBER and tipoDer == Tipo.NUMBER):
            return True
        
        if (tipoIzq == Tipo.STRING and tipoDer == Tipo.STRING):
            return True
        
        if (tipoIzq == Tipo.BOOL and tipoDer == Tipo.BOOL):
            return True
        
        if (tipoIzq == Tipo.ANY or tipoDer == Tipo.ANY):
            return True
    
    def check_labels(self):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        if self.trueLbl == '':
            self.trueLbl = generador.nuevoLbl()
        if self.falseLbl == '':
            self.falseLbl = generador.nuevoLbl()

    def getTipoOperacion(self):
        if self.tipo == TipoRelacionales.MAYOR:
            return '>'
        elif self.tipo == TipoRelacionales.MENOR:
            return '<'
        elif self.tipo == TipoRelacionales.MAYORIGUAL:
            return '>='
        elif self.tipo == TipoRelacionales.MENORIGUAL:
            return '<='
        elif self.tipo == TipoRelacionales.IGUALIGUAL:
            return '=='
        elif self.tipo == TipoRelacionales.DISTINTO:
            return '!='


