from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.GeneradorC3D import GeneradorC3D
from Sym.TablaSimbolos import TablaSimbolos
from Sym.Error import Error
from Instructions.Return import Return

class Funcion(Instruccion):
    def __init__(self, ident, listParametros, bloqInstrucciones, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.listParametros = listParametros
        self.bloqInstrucciones = bloqInstrucciones

    def compilar(self, env):
        env.guardarFuncion(self.ident, self)
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        generador.agregarComentario(f'Compilación de la función {self.ident}')

        nuevoEnv = TablaSimbolos(env)
        returnLbl = generador.nuevoLbl()
        nuevoEnv.returnLbl = returnLbl
        nuevoEnv.size = 1

        if self.listParametros != None:
            for param in self.listParametros:
                simbolo = nuevoEnv.guardarVar(param.ident, param.tipo, (param.tipo == Tipo.STRING))
            
        generador.agregarIniFunc(self.ident)

        for inst in self.bloqInstrucciones:
            instVal = inst.compilar(nuevoEnv)
            if isinstance(instVal, Error): return instVal

            if isinstance(instVal, Return):
                if instVal.getTrueLbl() == '':
                    generador.agregarComentario('Resultado retorno función')
                    generador.setStack('P', instVal.getValor())
                    generador.agregarGoTo(nuevoEnv.returnLbl)
                    generador.agregarComentario('Fin Resultado retorno función')
                else:
                    generador.agregarComentario('Resultado retorno función')
                    generador.putLbl(instVal.getTrueLbl())
                    generador.setStack('P', '1')
                    generador.agregarGoTo(nuevoEnv.returnLbl)
                    generador.putLbl(instVal.getFalseLbl())
                    generador.setStack('P', '0')
                    generador.agregarGoTo(nuevoEnv.returnLbl)
                    generador.agregarComentario('Fin Resultado retorno función')
        
        generador.agregarGoTo(returnLbl)
        generador.putLbl(returnLbl)

        generador.agregarComentario(f'Fin compilación de función {self.ident}')
        generador.agregarFinFunc()
        generador.agregarEspacio()
        return
    
    def getParams(self):
        return self.listParametros
    
    # def getTipo(self):
    #     return self.tipo

