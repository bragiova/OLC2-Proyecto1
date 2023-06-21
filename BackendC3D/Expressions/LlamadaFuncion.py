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
                a = param.compilar(env)
                if isinstance(a, Error): return a

                if isinstance(param, LlamadaFuncion):
                    self.guardarTemps(generador, env, temporales)
                    paramValores.append(a)
                    self.recuperarTemps(generador, env, temporales)
                else:
                    paramValores.append(a)
                    temporales.append(a.valor)
            
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

            return Retorno(Tipo.STRING, temp, True)
        
    def guardarTemps(self, generator, env, tmp2):
        generator.addComment('Guardado de temporales')
        tmp = generator.addTemp()
        for tmp1 in tmp2:
            generator.addExp(tmp, 'P', env.size, '+')
            generator.setStack(tmp,tmp1)
            env.size += 1
        generator.addComment('Fin de guardado de temporales')
    
    def recuperarTemps(self, generator, env, tmp2):
        generator.addComment('Recuperacion de Temporales')
        tmp = generator.addTemp()
        for tmp1 in tmp2:
            env.size -= 1
            generator.addExp(tmp, 'P', env.size, '+')
            generator.getStack(tmp1,tmp)
        generator.addComment('Fin de recuperacion de temporales')