
from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Simbolo import Simbolo
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class Declaracion(Instruccion):
    def __init__(self, ident, valor, tipo, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.valor = valor
        self.tipo = tipo
        self.find = True

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()

        generador.agregarComentario('Compilación valor de variable')
        valorVar = self.valor

        if valorVar is not None:
            valorVar = self.valor.compilar(env)
            if isinstance(valorVar, Error): return valorVar
            generador.agregarComentario('Fin Compilación valor de variable')
        else:
            if self.tipo is not None:
                valorVar = self.setValorDefecto(self.tipo)
            else:
                self.tipo = Tipo.ANY
                valorVar = Retorno(Tipo.ANY, None)

        if self.tipo == Tipo.ANY and self.tipo != valorVar.tipo:
            valorVar.tipo = Tipo.ANY

        if self.tipo == valorVar.tipo:
            nuevoSimbolo = env.guardarVar(self.ident, valorVar.tipo, (valorVar.tipo == Tipo.STRING), self.find)

            # if env.existeSimbEnActual(self.ident):
            #     return Error('Semántico', 'Variable ya está declarada', self.linea, self.columna)
            
            # env.guardarVar(nuevoSimbolo)
        else:
            return Error('Semántico', 'El tipo de dato de la variable es distinto a la asignación', self.linea, self.columna)
        
        tempPos = nuevoSimbolo.getPosicion()
        if not nuevoSimbolo.esGlobal:
            tempPos = generador.agregarTemp()
            generador.agregarExp(tempPos, 'P', nuevoSimbolo.getPosicion(), '+')

        if valorVar.tipo == Tipo.BOOL:
            tempLbl = generador.nuevoLbl()
            generador.putLbl(valorVar.trueLbl)
            generador.setStack(tempPos, '1')
            generador.agregarGoTo(tempLbl)
            generador.putLbl(valorVar.falseLbl)
            generador.setStack(tempPos, '0')
            generador.putLbl(tempLbl)
        else:
            generador.setStack(tempPos, valorVar.valor)
        
        generador.agregarEspacio()
        
    def setValorDefecto(self, tipo):
        if tipo == Tipo.NUMBER:
            return Retorno(Tipo.NUMBER, 0)
        elif tipo == Tipo.STRING:
            return Retorno(Tipo.STRING, "")
        elif tipo == Tipo.BOOL:
            return Retorno(Tipo.BOOL, 'false')
        elif tipo == Tipo.ANY:
            return Retorno(Tipo.ANY, None)



