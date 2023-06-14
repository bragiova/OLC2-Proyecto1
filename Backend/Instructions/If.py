from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error
from Sym.TablaSimbolos import TablaSimbolos

class If(Instruccion):
    def __init__(self, condicion, bloqIf, bloqElse, bloqElseIf, linea, columna):
        super().__init__(linea, columna)
        self.condicion = condicion
        self.bloqIf = bloqIf
        self.bloqElse = bloqElse
        self.bloqElseIf = bloqElseIf

    def ejecutar(self, env):
        condicionIf = self.condicion.ejecutar(env)
        # entorno = TablaSimbolos(env)

        if condicionIf.tipo != Tipo.BOOL:
            return Error('Semántico', 'La condición no es de tipo Boolean', self.linea, self.columna)
        
        if condicionIf.valor:
            entorno = TablaSimbolos(env)
            for instruccion in self.bloqIf:
                resultado = instruccion.ejecutar(entorno)
                if isinstance(resultado, Retorno):
                    if resultado.tipo == Tipo.RETURNST or resultado.tipo == Tipo.BREAKST or resultado.tipo == Tipo.CONTIST:
                        return resultado
                # TODO: FALTA VERIFICAR ERROR
        elif self.bloqElse is not None:
            entorno = TablaSimbolos(env)
            for instruccion in self.bloqElse:
                resultado = instruccion.ejecutar(entorno)
                if isinstance(resultado, Retorno):
                    if resultado.tipo == Tipo.RETURNST or resultado.tipo == Tipo.BREAKST or resultado.tipo == Tipo.CONTIST:
                        return resultado
        elif self.bloqElseIf is not None:
            # Se interpreta el objeto que se manda, ya que desde la gramática se manda un objeto If
            resultado = self.bloqElseIf.ejecutar(env)
            if isinstance(resultado, Retorno):
                    if resultado.tipo == Tipo.RETURNST or resultado.tipo == Tipo.BREAKST or resultado.tipo == Tipo.CONTIST:
                        return resultado


