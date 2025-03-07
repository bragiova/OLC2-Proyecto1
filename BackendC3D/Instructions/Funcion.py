from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.GeneradorC3D import GeneradorC3D
from Sym.TablaSimbolos import TablaSimbolos
from Sym.Error import Error
from Instructions.Return import Return

class Funcion(Instruccion):
    def __init__(self, ident, listParametros, bloqInstrucciones, tipoFuncion, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.listParametros = listParametros
        self.bloqInstrucciones = bloqInstrucciones
        self.tipoFuncion = tipoFuncion

    def compilar(self, env):
        env.guardarFuncion(self.ident, self)
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        generador.agregarComentario(f'Compilación de la funcion {self.ident}')

        nuevoEnv = TablaSimbolos(env)
        returnLbl = generador.nuevoLbl()
        nuevoEnv.returnLbl = returnLbl
        nuevoEnv.size = 1

        if self.listParametros != None:
            for param in self.listParametros:
                simbolo = nuevoEnv.guardarVar(param.ident, param.tipo, (param.tipo == Tipo.STRING), self.linea, self.columna)
            
        generador.agregarIniFunc(self.ident)

        for inst in self.bloqInstrucciones:
            instVal = inst.compilar(nuevoEnv)
            if isinstance(instVal, Error): return instVal

            if isinstance(instVal, Return):
                if instVal.getTrueLbl() == '':
                    generador.agregarComentario('Resultado retorno funcion')
                    generador.setStack('P', instVal.getValor())
                    generador.agregarGoTo(nuevoEnv.returnLbl)
                    generador.agregarComentario('Fin Resultado retorno funcion')
                else:
                    generador.agregarComentario('Resultado retorno funcion')
                    generador.putLbl(instVal.getTrueLbl())
                    generador.setStack('P', '1')
                    generador.agregarGoTo(nuevoEnv.returnLbl)
                    generador.putLbl(instVal.getFalseLbl())
                    generador.setStack('P', '0')
                    generador.agregarGoTo(nuevoEnv.returnLbl)
                    generador.agregarComentario('Fin Resultado retorno funcion')
        
        generador.agregarGoTo(returnLbl)
        generador.putLbl(returnLbl)

        generador.agregarComentario(f'Fin compilación de funcion {self.ident}')
        generador.agregarFinFunc()
        generador.agregarEspacio()
        return
    
    def getParams(self):
        return self.listParametros
    
    def getTipo(self):
        return self.tipoFuncion

