from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.TablaSimbolos import TablaSimbolos
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D
from Instructions.Return import Return

class While(Instruccion):
    def __init__(self, condicion, bloqInstrucciones, linea, columna):
        super().__init__(linea, columna)
        self.condicion = condicion
        self.bloqInstrucciones = bloqInstrucciones

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        generador.agregarComentario('Inicio While')

        lblLoop = generador.nuevoLbl()
        generador.putLbl(lblLoop)

        condicion = self.condicion.compilar(env)
        if isinstance(condicion, Error): return condicion

        generador.putLbl(condicion.trueLbl)
        env.breakLbl = condicion.falseLbl
        env.continueLbl = lblLoop

        if condicion.tipo != Tipo.BOOL:
            return Error('Semántico', 'Tipo de dato en la condición no es Boolean', self.linea, self.columna)
        
        for instruccion in self.bloqInstrucciones:
            entorno = TablaSimbolos(env)
            entorno.breakLbl = condicion.falseLbl
            entorno.continueLbl = lblLoop
            entorno.returnLbl = env.returnLbl

            resultado = instruccion.compilar(entorno)
            if isinstance(resultado, Error): return resultado

            if resultado is not None:
                if isinstance(resultado, Return):
                    if entorno.returnLbl != '':
                        if resultado.trueLbl == '':
                            generador.agregarComentario('Resultado Return While')
                            generador.setStack('P', resultado.valor)
                            generador.agregarGoTo(entorno.returnLbl)
                            generador.agregarComentario('Fin Return While')
                        else:
                            generador.agregarComentario('Resultado Return While')
                            generador.putLbl(resultado.trueLbl)
                            generador.setStack('P', '1')
                            generador.agregarGoTo(entorno.returnLbl)
                            generador.putLbl(resultado.falseLbl)
                            generador.setStack('P', '0')
                            generador.agregarGoTo(entorno.returnLbl)
                            generador.agregarComentario('Fin Return While')                        
                elif isinstance(resultado, Retorno):
                    if resultado.tipo == Tipo.BREAKST:
                        generador.agregarGoTo(condicion.falseLbl)
                        break
                    elif resultado.tipo == Tipo.CONTIST:
                        generador.agregarGoTo(lblLoop)
                
        env.breakLbl = ''
        env.continueLbl = ''
        
        generador.agregarGoTo(lblLoop)
        generador.putLbl(condicion.falseLbl)
        generador.agregarComentario('Fin While')

        


