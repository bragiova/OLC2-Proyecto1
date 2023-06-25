
from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class ImprimirClg(Instruccion):
    salidaConsola = ''

    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        super().__init__(linea, columna)

    def compilar(self, env):
        txtImprimir = ''

        genAux = GeneradorC3D()
        generador = genAux.getInstancia()

        for expre in self.expresion:
            expreVal = expre.compilar(env)
            if isinstance(expreVal, Error): return expreVal

            if expreVal.tipo == Tipo.NUMBER:
                generador.agregarPrint('f', expreVal.valor)
                # if isinstance(expreVal.valor, int):
                #     generador.agregarPrint('d', expreVal.valor)
                # else:
                #     generador.imprimirFloat('f', expreVal.valor)
            elif expreVal.tipo == Tipo.STRING:
                generador.fPrintString()
                paramTemp = generador.agregarTemp()
                generador.agregarExp(paramTemp, 'P', env.size, '+')
                generador.agregarExp(paramTemp, paramTemp, '1', '+')
                generador.setStack(paramTemp, expreVal.valor)

                generador.nuevoEnv(env.size)
                generador.llamadaFun('printString')

                temp = generador.agregarTemp()
                generador.getStack(temp, 'P')
                generador.returnEnv(env.size)
            elif expreVal.tipo == Tipo.BOOL:
                lblTemp = generador.nuevoLbl()
                generador.putLbl(expreVal.trueLbl)
                generador.imprimirTrue()
                generador.agregarGoTo(lblTemp)
                generador.putLbl(expreVal.falseLbl)
                generador.imprimirFalse()
                generador.putLbl(lblTemp)
            
            generador.agregarPrint('c', 10)
            # txtImprimir += str(expreVal.valor) + ' '
        
        # print(txtImprimir)
        # Se crea una variable global para ir concatenando todo lo que debe imprimirse en consola
        # ImprimirClg.salidaConsola += txtImprimir + '\n'
        # return Retorno(Tipo.STRING, txtImprimir)