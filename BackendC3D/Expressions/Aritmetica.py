
from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from enum import Enum
from Sym.Error import Error
from Sym.GeneradorC3D import GeneradorC3D

class TipoOperacionAritmetica(Enum):
    SUMA = 1
    RESTA = 2
    MULTI = 3
    DIV = 4
    MOD = 5
    POT = 6

class Aritmetica(Expresion):
    def __init__(self, opeIzq, opeDer, operacion, linea, columna):
        self.opIzq = opeIzq
        self.opDer = opeDer
        self.operacion = operacion
        super().__init__(linea, columna)

    def compilar(self, env):
        genAux = GeneradorC3D()
        generador = genAux.getInstancia()
        # Se ejecuta el método de Primitivo, que obtiene el valor del operando
        opIzq = self.opIzq.compilar(env)
        if isinstance(opIzq, Error): return opIzq
        opDer = self.opDer.compilar(env)
        if isinstance(opDer, Error): return opDer
        
        if opIzq.tipo == Tipo.RETURNST:
            if isinstance(opIzq.valor, int) or isinstance(opIzq.valor, float):
                opIzq.tipo = Tipo.NUMBER
            elif isinstance(opIzq.valor, str):
                opIzq.tipo = Tipo.STRING
        
        if opDer.tipo == Tipo.RETURNST:
            if isinstance(opDer.valor, int) or isinstance(opDer.valor, float):
                opDer.tipo = Tipo.NUMBER
            elif isinstance(opIzq.valor, str):
                opIzq.tipo = Tipo.STRING

        # Se inicializa el objeto Resultado con el tipo Number por defecto
        resultado = Retorno(Tipo.NUMBER, 0, True)
        esPermitido = self.esTipoPermitido(opIzq.tipo, opDer.tipo)

        if self.operacion == TipoOperacionAritmetica.SUMA:
            if esPermitido:
                if opIzq.tipo == Tipo.NUMBER and opDer.tipo == Tipo.NUMBER:
                    temp = generador.agregarTemp()
                    generador.agregarExp(temp, opIzq.valor, opDer.valor, '+')
                elif opIzq.tipo == Tipo.STRING and opDer.tipo == Tipo.STRING:
                    left_temp = generador.agregarTemp()
                    right_temp = generador.agregarTemp()
                    ret_temp = generador.agregarTemp()
                    auxiliar_temp = generador.agregarTemp()
                    generador.agregarExp(ret_temp, 'H', '', '')
                    generador.agregarExp(
                        left_temp, opIzq.valor, '', '')
                    generador.agregarExp(
                        right_temp, opDer.valor, '', '')
                    generador.agregarExp(
                        auxiliar_temp, opIzq.valor, '', '')
                    
                    left_label = generador.nuevoLbl()
                    right_label = generador.nuevoLbl()
                    left_swaper = generador.agregarTemp()
                    right_swaper = generador.agregarTemp()
                    generador.getHeap(left_swaper, left_temp)
                    generador.getHeap(right_swaper, right_temp)

                    generador.putLbl(left_label)
                    generador.setHeap('H', left_swaper)
                    generador.nextHeap()
                    generador.agregarExp(left_temp, left_temp, '1', '+')
                    generador.getHeap(left_swaper, left_temp)
                    generador.agregarIf(left_swaper, '-1', '!=', left_label)

                    generador.putLbl(right_label)
                    generador.setHeap('H', right_swaper)
                    generador.nextHeap()
                    generador.agregarExp(right_temp, right_temp, '1', '+')
                    generador.getHeap(right_swaper, right_temp)
                    generador.agregarIf(right_swaper, '-1', '!=', right_label)
                    generador.setHeap('H', '-1')
                    generador.nextHeap()
                # Se cambia tipo del resultado si son string operandos, operador ternario
                resultado.tipo = (Tipo.STRING if (opIzq.tipo == Tipo.STRING and opDer.tipo == Tipo.STRING) else resultado.tipo)
                resultado.esTemp = False
            else:
                print('Error en tipo de dato - suma')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación suma', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.RESTA:
            if esPermitido:
                temp = generador.agregarTemp()
                generador.agregarExp(temp, opIzq.valor, opDer.valor, '-')
            else:
                print('Error en tipo de dato - resta')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación resta', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.MULTI:
            if esPermitido:
                temp = generador.agregarTemp()
                generador.agregarExp(temp, opIzq.valor, opDer.valor, '*')
            else:
                print('Error en tipo de dato - multiplicación')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación multiplicación', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.DIV:
            if esPermitido:
                temp = generador.agregarTemp()
                generador.agregarExp(temp, opIzq.valor, opDer.valor, '/')
            else:
                print('Error en tipo de dato - división')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación división', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.MOD:
            if esPermitido:
                temp = generador.agregarTemp()
                generador.agregarModulo(temp, opIzq.valor, opDer.valor)
            else:
                print('Error en tipo de dato - módulo')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación módulo', self.linea, self.columna)
        elif self.operacion == TipoOperacionAritmetica.POT:
            if esPermitido:
                temp = generador.agregarTemp()
                generador.agregarExp(temp, opIzq.valor, opDer.valor, '^')
            else:
                print('Error en tipo de dato - potencia')
                return Error('Semántico', 'El tipo de dato no es permitido para la operación potencia', self.linea, self.columna)
        else:
            print('Error operacion')
            return Error('Semántico', 'El tipo de operación no es permitido para operaciones aritméticas', self.linea, self.columna)
        
        return resultado
    
    def esTipoPermitido(self, tipoIzq, tipoDer):
        if (tipoIzq == Tipo.NUMBER and tipoDer == Tipo.NUMBER):
            return True
        
        if (tipoIzq == Tipo.STRING and tipoDer == Tipo.STRING):
            return True
        
        if (tipoIzq == Tipo.ANY or tipoDer == Tipo.ANY):
            return True
