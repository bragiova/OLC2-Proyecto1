from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Simbolo import Simbolo
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class Asignacion(Instruccion):
    def __init__(self, ident, valor, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.valor = valor

    def compilar(self, env):
        simbVar = env.getSimbolo(self.ident)
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()

        generador.agregarComentario('Compilación asignacion de variable')

        if simbVar is not None:
            temp = generador.agregarTemp()

            tempPos = simbVar.getPosicion()
            if not simbVar.esGlobal:
                tempPos = generador.agregarTemp()
                generador.agregarExp(tempPos, 'P', simbVar.getPosicion(), '+')
            generador.getStack(temp, tempPos)

            tmp = generador.agregarTemp()

            valVariable = self.valor.compilar(env)
            if isinstance(valVariable, Error): return valVariable

            if valVariable.tipo == Tipo.BOOL:
                tempLbl = generador.nuevoLbl()
                generador.putLbl(valVariable.trueLbl)
                generador.setStack(tempPos, '1')
                generador.agregarGoTo(tempLbl)
                generador.putLbl(valVariable.falseLbl)
                generador.setStack(tempPos, '0')
                generador.putLbl(tempLbl)
            else:
                generador.setStack(tempPos, valVariable.valor)

            generador.agregarComentario('Fin Compilación asignacion de variable')
            generador.agregarEspacio()

        else:
            return Error('Semántico', 'Variable no existe', self.linea, self.columna)
