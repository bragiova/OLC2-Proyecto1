from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class UpperCase(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()

        expreUp = self.expresion.compilar(env)
        if isinstance(expreUp, Error): return expreUp

        resultado = Retorno(Tipo.STRING, '', True)

        if expreUp is not None:
            generador.fUpperCase()
            temp = generador.agregarTemp()
            generador.agregarExp(temp, 'P', env.size, '+')
            generador.agregarExp(temp, temp, '1', '+')
            generador.setStack(temp, expreUp.valor)
            generador.nuevoEnv(env.size)
            generador.llamadaFun('uppercase')
            
            tmp1 = generador.agregarTemp()
            tmp2 = generador.agregarTemp()
            generador.agregarExp(tmp2, 'P', '1', '+')
            generador.getStack(tmp1, tmp2)
            resultado.valor = tmp1
        
        return resultado
        

