from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class Length(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()

        valLength = self.expresion.compilar(env)
        if isinstance(valLength, Error): return Error

        resultado = Retorno(Tipo.NUMBER, 0, True)

        if valLength is not None:
            temp = generador.agregarTemp()
            generador.fLength()

            tmp1 = generador.agregarTemp()
            generador.agregarExp(tmp1, 'P', env.size, '+')
            generador.agregarExp(tmp1, tmp1, '1', '+')

            generador.setStack(tmp1, valLength.valor)
            # generador.agregarExp(tmp1, tmp1, '1', '+')
            
            generador.nuevoEnv(env.size)
            generador.llamadaFun('length')
            
            # tmp2 = generador.agregarTemp()
            # generador.agregarExp(tmp2, 'P', '1', '+')
            # generador.getStack(tmp1, tmp2)
            generador.getStack(temp, 'P')
            generador.returnEnv(env.size)
            resultado.valor = tmp1
        else:
            return Error('Semántico', 'El tipo no es aplicable a la función length', self.linea, self.columna)
        
        return resultado