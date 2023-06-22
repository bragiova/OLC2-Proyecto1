from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error
from Sym.TablaSimbolos import TablaSimbolos
from Sym.GeneradorC3D import GeneradorC3D

class If(Instruccion):
    def __init__(self, condicion, bloqIf, bloqElse, bloqElseIf, linea, columna):
        super().__init__(linea, columna)
        self.condicion = condicion
        self.bloqIf = bloqIf
        self.bloqElse = bloqElse
        self.bloqElseIf = bloqElseIf

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        generador.agregarComentario('Inicio If')

        condicionIf = self.condicion.compilar(env)
        if isinstance(condicionIf, Error): return condicionIf
        # entorno = TablaSimbolos(env)

        if condicionIf.tipo != Tipo.BOOL:
            return Error('Semántico', 'La condición no es de tipo Boolean', self.linea, self.columna)
        
        generador.putLbl(condicionIf.trueLbl)
        entorno = TablaSimbolos(env)

        for instruccion in self.bloqIf:
            entorno.breakLbl = env.breakLbl
            entorno.returnLbl = env.returnLbl
            entorno.continueLbl = env.continueLbl

            resultado = instruccion.compilar(entorno)
            if isinstance(resultado, Error): return resultado

            if isinstance(resultado, Retorno):
                if resultado.tipo == Tipo.RETURNST:
                    if entorno.returnLbl != '':
                        if resultado.getTrueLbl() == '':
                            generador.agregarComentario('Resultado retorno función')
                            generador.setStack('P', resultado.valor)
                            generador.agregarGoTo(entorno.returnLbl)
                            generador.agregarComentario('Fin resultado retorno función')
                        else:
                            generador.agregarComentario('Resultado retorno función')
                            generador.putLbl(resultado.trueLbl)
                            generador.setStack('P', '1')
                            generador.agregarGoTo(entorno.returnLbl)
                            generador.putLbl(resultado.falseLbl)
                            generador.setStack('P', '0')
                            generador.agregarGoTo(entorno.returnLbl)
                            generador.agregarComentario('Fin resultado retorno función')
                
                if resultado.tipo == Tipo.BREAKST:
                    if env.breakLbl != '':
                        generador.agregarGoTo(env.breakLbl)
                    else:
                        salida = generador.nuevoLbl()
                        generador.agregarGoTo(salida)
                        generador.putLbl(condicionIf.falseLbl)
                        generador.putLbl(salida)
                        return Error('Semántico', 'Break solamente debe de ir en un ciclo', self.linea, self.columna)
                
                if resultado.tipo == Tipo.CONTIST:
                    if env.continueLbl != '':
                        generador.agregarGoTo(env.continueLbl)
                    else:
                        salida = generador.nuevoLbl()
                        generador.agregarGoTo(salida)
                        generador.putLbl(condicionIf.falseLbl)
                        generador.putLbl(salida)
                        return Error('Semántico', 'Continue solamente debe de ir en un ciclo', self.linea, self.columna)
        
        salir = generador.nuevoLbl()
        generador.agregarGoTo(salir)
        generador.putLbl(condicionIf.falseLbl)
                
        if self.bloqElse is not None:
            entorno = TablaSimbolos(env)
            for instruccion in self.bloqElse:
                entorno.breakLbl = env.breakLbl
                entorno.returnLbl = env.returnLbl
                entorno.continueLbl = env.continueLbl

                resultado = instruccion.compilar(entorno)
                if isinstance(resultado, Error): return resultado

                if isinstance(resultado, Retorno):
                    if resultado.tipo == Tipo.RETURNST:
                        if entorno.returnLbl != '':
                            if resultado.getTrueLbl() == '':
                                generador.agregarComentario('Resultado retorno función')
                                generador.setStack('P', resultado.valor)
                                generador.agregarGoTo(entorno.returnLbl)
                                generador.agregarComentario('Fin resultado retorno función')
                            else:
                                generador.agregarComentario('Resultado retorno función')
                                generador.putLbl(resultado.trueLbl)
                                generador.setStack('P', '1')
                                generador.agregarGoTo(entorno.returnLbl)
                                generador.putLbl(resultado.falseLbl)
                                generador.setStack('P', '0')
                                generador.agregarGoTo(entorno.returnLbl)
                                generador.agregarComentario('Fin resultado retorno función')
                    
                    if resultado.tipo == Tipo.BREAKST:
                        if env.breakLbl != '':
                            generador.agregarGoTo(env.breakLbl)
                        else:
                            salida = generador.nuevoLbl()
                            generador.agregarGoTo(salida)
                            generador.putLbl(condicionIf.falseLbl)
                            generador.putLbl(salida)
                            return Error('Semántico', 'Break solamente debe de ir en un ciclo', self.linea, self.columna)
                    
                    if resultado.tipo == Tipo.CONTIST:
                        if env.continueLbl != '':
                            generador.agregarGoTo(env.continueLbl)
                        else:
                            salida = generador.nuevoLbl()
                            generador.agregarGoTo(salida)
                            generador.putLbl(condicionIf.falseLbl)
                            generador.putLbl(salida)
                            return Error('Semántico', 'Continue solamente debe de ir en un ciclo', self.linea, self.columna)
                    
        elif self.bloqElseIf is not None:
            # Se interpreta el objeto que se manda, ya que desde la gramática se manda un objeto If
            resultado = self.bloqElseIf.compilar(env)
            if isinstance(resultado, Error): return resultado
            
        generador.putLbl(salir)
        generador.agregarComentario('Fin If')


