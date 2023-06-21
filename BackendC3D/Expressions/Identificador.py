
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class Identificador(Expresion):
    def __init__(self, ident, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        
        generador.agregarComentario('Compilación acceso')
        variable = env.getSimbolo(self.ident)

        if variable is None:
            generador.agregarComentario('Fin compilación acceso - error')
            return Error('Semántico', 'Variable no encontrada', self.linea, self.columna)
        
        # Temp para guardar variable
        temp = generador.agregarTemp()

        # Se obtiene posición de variable
        tempPos = variable.posicion
        if not variable.esGlobal:
            tempPos = generador.agregarTemp()
            generador.agregarExp(tempPos, 'P', variable.posicion, '+')
        generador.getStack(temp, tempPos)

        if variable.tipo != Tipo.BOOL:
            generador.agregarComentario('Fin compilación acceso')
            generador.agregarEspacio()
            return Retorno(variable.tipo, temp, True)
        
        if self.trueLbl == '':
            self.trueLbl = generador.nuevoLbl()

        if self.falseLbl == '':
            self.falseLbl = generador.nuevoLbl()

        generador.agregarIf(temp, '1', '==', self.trueLbl)
        generador.agregarGoTo(self.falseLbl)

        generador.agregarComentario('Fin compilación acceso')
        generador.agregarEspacio()

        result = Retorno(Tipo.BOOL, None, False)
        result.trueLbl = self.trueLbl
        result.falseLbl = self.falseLbl

        return result
