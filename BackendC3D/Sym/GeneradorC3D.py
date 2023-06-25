
class GeneradorC3D:
    generator = None
    heap = [0 for i in range(3010199)]
    stack = [0 for i in range(3010199)]
    dict_temp = {'H': 0, 'P': 0, '': 0}

    def __init__(self):
        # contadores
        self.contTemp = 0
        self.contLbl = 0
        # código
        self.codigo = ''
        self.funcs = ''
        self.nativas = ''
        self.enFunc = False
        self.enNativa = False
        # Lista de temporales
        self.temporales = []
        # Lista nativas
        self.printString = False
        self.compararString = False
        self.concatString = False
        self.upperCase = False
        self.lowerCase = False
        self.potencia = False
        self.length = False

        self.modulo = False

    def limpiarTodo(self):
        self.contTemp = 0
        self.contLbl = 0
        self.codigo = ''
        self.funcs = ''
        self.nativas = ''
        self.enFunc = False
        self.enNativa = False
        self.temporales = []
        self.printString = False
        self.compararString = False
        self.concatString = False
        self.upperCase = False
        self.lowerCase = False
        self.potencia = False
        self.length = False
        GeneradorC3D.generator = GeneradorC3D()

    def getHeader(self):
        result = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"\n)\n\n'
        
        if self.modulo:
            result = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"\n\t"math"\n)\n\n'

        if len(self.temporales) > 0:
            result += 'var '
            for temp in range(len(self.temporales)):
                result += self.temporales[temp]
                if temp != (len(self.temporales) - 1):
                    result += ', '
            result += ' float64;\n'
        result += 'var P, H float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n'
        return result
    
    def getCodigo(self):
        return f'{self.getHeader()}{self.nativas}\n{self.funcs}\nfunc main(){{\n{self.codigo}\n}}'
    
    def codigoEn(self, codigo, tab='\t'):
        if self.enNativa:
            if self.nativas == '':
                self.nativas += '/*-----NATIVAS-----*/\n'
            self.nativas += tab + codigo
        elif self.enFunc:
            if self.funcs == '':
                self.funcs += '/*-----FUNCS-----*/\n'
            self.funcs += tab + codigo
        else:
            self.codigo += '\t' + codigo
    
    def agregarComentario(self, comentario):
        self.codigoEn(f'/* {comentario} */\n')

    def agregarEspacio(self):
        self.codigoEn('\n')
    
    def getInstancia(self):
        if GeneradorC3D.generator == None:
            GeneradorC3D.generator = GeneradorC3D()
        return GeneradorC3D.generator

    # Manejo de temporales
    def agregarTemp(self):
        # GeneradorC3D.dict_temp[f't{self.contTemp}'] = 0
        temp = f't{self.contTemp}'
        self.contTemp += 1
        self.temporales.append(temp)
        return temp # se agrega nuevo temp t0 t1 t2 t3 ...
    
    # Manejo de Labels
    def nuevoLbl(self):
        label = f'L{self.contLbl}'
        self.contLbl += 1
        return label # se agrega nuevo label L0 L1 L2 ...
    
    def putLbl(self, label):
        self.codigoEn(f'{label}:\n') # L1: L2: L3: ...

    # GOTO
    def agregarGoTo(self, label):
        self.codigoEn(f'goto {label};\n')

    # IF
    def agregarIf(self, izq, der, ope, label):
        self.codigoEn(f'if {izq} {ope} {der} {{goto {label};}}\n')
    
    # Expresiones
    def agregarExp(self, resultado, izq, der, ope):
        self.codigoEn(f'{resultado} = {izq} {ope} {der};\n')
    
    def agregarAsig(self, resultado, izq):
        self.codigoEn(f'{resultado} = {izq};\n')

    # Funciones
    def agregarIniFunc(self, ident):
        if not self.enNativa:
            self.enFunc = True
        self.codigoEn(f'func {ident}(){{\n', '')
    
    def agregarFinFunc(self):
        self.codigoEn('return;\n}\n')
        if not self.enNativa:
            self.enFunc = False

    # STACK
    def setStack(self, pos, valor):
        self.codigoEn(f'stack[int({pos})] = {valor};\n')
    
    def getStack(self, lugar, pos):
        self.codigoEn(f'{lugar} = stack[int({pos})];\n')

    # Entorno
    def nuevoEnv(self, size):
        self.codigoEn(f'/* --- NUEVO ENTORNO --- */\n')
        self.codigoEn(f'P = P + {size};\n')
    
    def llamadaFun(self, ident):
        self.codigoEn(f'{ident}();\n')

    def returnEnv(self, size):
        self.codigoEn(f'P = P - {size};\n')

    # HEAP
    def setHeap(self, pos, valor):
        self.codigoEn(f'heap[int({pos})] = {valor};\n')
    
    def getHeap(self, lugar, pos):
        self.codigoEn(f'{lugar} = heap[int({pos})];\n')

    def nextHeap(self):
        self.codigoEn('H = H + 1;\n')
    
    # Instrucciones
    def agregarPrint(self, tipo, valor):
        self.codigoEn(f'fmt.Printf("%{tipo}", {valor});\n')
    
    def agregarPrintChar(self, tipo, valor):
        self.codigoEn(f'fmt.Printf("%{tipo}", int({valor}));\n')

    def imprimirFloat(self, tipo, valor):
        self.codigoEn(f'fmt.Printf("%{tipo}", {valor});\n')

    def imprimirTrue(self):
        self.agregarPrint('c', 116)
        self.agregarPrint('c', 114)
        self.agregarPrint('c', 117)
        self.agregarPrint('c', 101)

    def imprimirFalse(self):
        self.agregarPrint('c', 102)
        self.agregarPrint('c', 97)
        self.agregarPrint('c', 108)
        self.agregarPrint('c', 115)
        self.agregarPrint('c', 101)

    # Nativas
    def fPrintString(self):
        if self.printString:
            return

        self.printString = True
        self.enNativa = True

        self.agregarIniFunc('printString')

        # Label para salir de función
        returnLbl = self.nuevoLbl()
        # Label de comparación para buscar fin de cadena
        compLbl = self.nuevoLbl()
        # Temp puntero a Stack
        tempS = self.agregarTemp()
        # Temp puntero a Heap
        tempH = self.agregarTemp()

        self.agregarExp(tempS, 'P', '1', '+')
        self.getStack(tempH, tempS)

        # Temp para comparar
        tempComp = self.agregarTemp()

        self.putLbl(compLbl)
        self.getHeap(tempComp, tempH)

        self.agregarIf(tempComp, '-1', '==', returnLbl)
        self.agregarPrintChar('c', tempComp)
        self.agregarExp(tempH, tempH, '1', '+')
        self.agregarGoTo(compLbl)
        self.putLbl(returnLbl)
        self.agregarFinFunc()
        self.enNativa = False
    
    def fcompararString(self):
        if self.compararString:
            return
        
        self.compararString = True
        self.enNativa = True

        self.agregarIniFunc('compararString')
        returnLbl = self.nuevoLbl()

        t2 = self.agregarTemp()
        self.agregarExp(t2, 'P', '1', '+')
        t3 = self.agregarTemp()
        self.getStack(t3, t2)
        self.agregarExp(t2, t2, '1', '+')
        t4 = self.agregarTemp()
        self.getStack(t4, t2)

        lbl1 = self.nuevoLbl()
        lbl2 = self.nuevoLbl()
        lbl3 = self.nuevoLbl()
        self.putLbl(lbl1)

        t5 = self.agregarTemp()
        self.getHeap(t5, t3)

        t6 = self.agregarTemp()
        self.getHeap(t6, t4)

        self.agregarIf(t5, t6, '!=', lbl3)
        self.agregarIf(t5, '-1', '==', lbl2)

        self.agregarExp(t3, t3, '1', '+')
        self.agregarExp(t4, t4, '1', '+')
        self.agregarGoTo(lbl1)

        self.putLbl(lbl2)
        self.setStack('P', '1')
        self.agregarGoTo(returnLbl)
        self.putLbl(lbl3)
        self.setStack('P', '0')
        self.putLbl(returnLbl)
        self.agregarFinFunc()
        self.enNativa = False

    def fUpperCase(self):
        if self.upperCase:
            return
        
        self.upperCase = True
        self.enNativa = True
        
        self.agregarIniFunc('uppercase')
        
        returnLbl = self.nuevoLbl()
        compLbl = self.nuevoLbl()
        tempP = self.agregarTemp()
        tempH = self.agregarTemp()

        self.agregarExp(tempP, 'P', '1', '+')
        self.getStack(tempH, tempP)

        tempC = self.agregarTemp()
        self.putLbl(compLbl)
        self.getHeap(tempC, tempH)
        self.agregarIf(tempC, '-1', '==', returnLbl)

        temp = self.agregarTemp()
        passLbl = self.nuevoLbl()
        
        self.agregarIf(tempC, '97', '<', passLbl)
        self.agregarIf(tempC, '122', '>', passLbl)
        self.agregarExp(temp, tempC,'32', '-')
        self.setHeap(tempH, temp)
        self.putLbl(passLbl)

        self.agregarExp(tempH, tempH, '1', '+')

        self.agregarGoTo(compLbl)

        self.putLbl(returnLbl)
        self.agregarFinFunc()

        self.enNativa = False

    def fLowerCase(self):
        if self.lowerCase:
            return
        
        self.lowerCase = True
        self.enNativa = True
        
        self.agregarIniFunc('lowercase')
        
        returnLbl = self.nuevoLbl()
        compLbl = self.nuevoLbl()
        tempP = self.agregarTemp()
        tempH = self.agregarTemp()

        self.agregarExp(tempP, 'P', '1', '+')
        self.getStack(tempH, tempP)

        tempC = self.agregarTemp()
        self.putLbl(compLbl)
        self.getHeap(tempC, tempH)
        self.agregarIf(tempC, '-1', '==', returnLbl)

        temp = self.agregarTemp()
        passLbl = self.nuevoLbl()
        
        self.agregarIf(tempC, '65', '<', passLbl)
        self.agregarIf(tempC, '90', '>', passLbl)
        self.agregarExp(temp, tempC,'32', '+')
        self.setHeap(tempH, temp)
        self.putLbl(passLbl)

        self.agregarExp(tempH, tempH, '1', '+')

        self.agregarGoTo(compLbl)

        self.putLbl(returnLbl)
        self.agregarFinFunc()

        self.enNativa = False

    def fconcatString(self):
        if self.concatString:
            return
        
        self.concatString = True
        self.enNativas = True

        self.agregarIniFunc('concatString')
        
        returnLbl = self.nuevoLbl()
        lbl1 = self.nuevoLbl()
        lbl2 = self.nuevoLbl()
        lbl3 = self.nuevoLbl()
        t3 = self.agregarTemp()
        t4 = self.agregarTemp()
        t5 = self.agregarTemp()
        t6 = self.agregarTemp()
        t7 = self.agregarTemp()

        self.agregarExp(t3, 'H',"","")
        self.agregarExp(t4,'P','1','+')
        self.getStack(t6, t4)
        self.agregarExp(t5, 'P', '2', '+')

        self.putLbl(lbl1)

        self.getHeap(t7, t6)
        self.agregarIf(t7, '-1','==', lbl2)
        self.setHeap('H', t7)
        self.agregarExp('H', 'H','1','+')
        self.agregarExp(t6,t6,'1', '+')
        self.agregarGoTo(lbl1)

        self.putLbl(lbl2)

        self.getStack(t6,t5)

        self.putLbl(lbl3)
        self.getHeap(t7, t6)
        self.agregarIf(t7, '-1','==', returnLbl)
        self.setHeap('H', t7)
        self.agregarExp('H', 'H','1','+')
        self.agregarExp(t6,t6,'1', '+')
        self.agregarGoTo(lbl3)

        self.putLbl(returnLbl)
        self.setHeap('H', '-1')
        self.agregarExp('H', 'H','1', '+')
        self.setStack('P', t3)
        self.agregarFinFunc()
        self.enNativas = False
    
    def fPotencia(self):
        if self.potencia:
            return
        
        self.potencia = True
        self.enNativa = True
        self.agregarIniFunc('potencia')

        # Labels a utilizar
        lbl0 = self.nuevoLbl()
        lbl1 = self.nuevoLbl()
        lbl2 = self.nuevoLbl()
        lbl3 = self.nuevoLbl()

        # Temporales a utilizar
        t1 = self.agregarTemp()
        t2 = self.agregarTemp()
        t3 = self.agregarTemp()
        t4 = self.agregarTemp()

        #Escritura del codigo
        self.agregarExp(t2, 'P', '1','+')
        self.getStack(t1, t2)
        self.agregarExp(t3,t1,'','')
        self.agregarExp(t4,t1,'','')
        self.agregarExp(t2,'P','2','+')
        self.getStack(t1,t2)
        self.agregarIf(t1,'0','==', lbl1)
        self.putLbl(lbl2)
        self.agregarIf(t1, '1','<=',lbl0)
        self.agregarExp(t3, t3,t4,'*')
        self.agregarExp(t1,t1,'1', '-')
        self.agregarGoTo(lbl2)
        self.putLbl(lbl0)
        self.setStack('P', t3)
        self.agregarGoTo(lbl3)
        self.putLbl(lbl1)
        self.setStack('P', '1')
        self.putLbl(lbl3)
        self.agregarFinFunc()
        self.agregarEspacio()
        self.enNativa = False

    def fLength(self):
        if self.length:
            return
        
        self.length = True
        self.enNativa = True
        self.agregarIniFunc('length')

        returnLbl = self.nuevoLbl()
        compLbl = self.nuevoLbl()

        # Temporal puntero en Stack
        temp = self.agregarTemp()
        # Temporal puntero en Heap
        tempH = self.agregarTemp()

        tempR = self.agregarTemp()
        
        # Posición en Stack
        self.agregarExp(temp, 'P', '1', '+')
        self.getStack(tempH, temp)

        self.agregarExp(tempR, '0', '', '')

        # Temporal resultado
        tempC = self.agregarTemp()
        self.putLbl(compLbl)
        # Posición en el Heap
        self.getHeap(tempC, tempH)

        self.agregarIf(tempC, '-1', '==', returnLbl)

        # resultLbl = self.nuevoLbl()
        self.agregarExp(tempR, tempR, '1', '+')
        # self.putLbl(resultLbl)

        self.agregarExp(tempH, tempH, '1', '+')
        self.setStack('P', tempR)
        self.agregarGoTo(compLbl)

        self.putLbl(returnLbl)
        self.agregarFinFunc()
        self.enNativa = False

    def agregarModulo(self, resultado, izq, der):
        self.modulo = True
        self.codigoEn(f'{resultado} = math.Mod({izq},{der});\n')

    def operaciones(self, izq, der, ope):
        try:
            if(ope == '+'):
                return izq + der
            elif(ope == '-'):
                return izq - der
            elif(ope == '*'):
                return izq * der
            elif(ope == '/'):
                return izq / der
            elif(ope == '%'):
                return izq % der
            else:
                return izq
        except:
            return izq