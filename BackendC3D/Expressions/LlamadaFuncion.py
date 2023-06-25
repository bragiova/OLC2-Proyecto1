from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from Instructions.Return import Return
from Sym.TablaSimbolos import TablaSimbolos
from Sym.Simbolo import Simbolo
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class LlamadaFuncion(Expresion):
    def __init__(self, ident, listaParams, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.listaParams = listaParams
        self.trueLbl = ''
        self.falseLbl = ''

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        # se busca la función
        funcion = env.getFuncion(self.ident)
        
        if funcion is not None:
            generador.agregarComentario(f'Llamada de la función {self.ident}')
            paramValores = []
            temporales = []
            size = env.size

            # Recorremos el arreglo de parámetros
            for i, param in enumerate(self.listaParams):
                paramArr = param.compilar(env)
                if isinstance(paramArr, Error): return paramArr

                if isinstance(param, LlamadaFuncion):
                    self.guardarTemps(generador, env, temporales)
                    paramValores.append(paramArr)
                    self.recuperarTemps(generador, env, temporales)
                else:
                    paramValores.append(paramArr)
                    temporales.append(paramArr.valor)
            
            temp = generador.agregarTemp()
            generador.agregarExp(temp, 'P', size + 1, '+')
            aux = 0

            if len(funcion.getParams()) == len(paramValores):
                for param in paramValores:
                    aux += 1
                    generador.setStack(temp, param.valor)
                    if aux != len(paramValores):
                        generador.agregarExp(temp, temp, '1', '+')

            generador.nuevoEnv(size)
            generador.llamadaFun(self.ident)
            generador.getStack(temp, 'P')
            generador.returnEnv(size)
            generador.agregarComentario(f"Fin de la llamada a la funcion {self.ident}")
            generador.agregarEspacio()

            if funcion.tipoFuncion != Tipo.BOOL:
                return Retorno(funcion.tipoFuncion, temp, True)
            else:
                generador.agregarComentario('Recuperacion bool')

                if self.trueLbl == '':
                    self.trueLbl = generador.nuevoLbl()
                
                if self.falseLbl == '':
                    self.falseLbl = generador.nuevoLbl()
                
                generador.agregarIf(temp, '1', '==', self.trueLbl)
                generador.agregarGoTo(self.falseLbl)
                result = Retorno(funcion.tipoFuncion, temp, True)
                result.trueLbl = self.trueLbl
                result.falseLbl = self.falseLbl
                generador.agregarComentario('Fin recuperacion bool')
                return result
        
    def guardarTemps(self, generator, env, tmp2):
        generator.agregarComentario('Guardado de temporales')
        tmp = generator.agregarTemp()
        for tmp1 in tmp2:
            generator.agregarExp(tmp, 'P', env.size, '+')
            generator.setStack(tmp, tmp1)
            env.size += 1
        generator.agregarComentario('Fin de guardado de temporales')
    
    def recuperarTemps(self, generator, env, tmp2):
        generator.agregarComentario('Recuperacion de Temporales')
        tmp = generator.agregarTemp()
        for tmp1 in tmp2:
            env.size -= 1
            generator.agregarExp(tmp, 'P', env.size, '+')
            generator.getStack(tmp1, tmp)
        generator.agregarComentario('Fin de recuperacion de temporales')