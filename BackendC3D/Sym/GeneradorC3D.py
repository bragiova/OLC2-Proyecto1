
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
        GeneradorC3D.generator = GeneradorC3D()

    def getHeader(self):
        result = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"\n)\n\n'
        # TODO: importación con math
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
                self.nativas += '/*-----NATIVES-----*/\n'
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
        # if izq in GeneradorC3D.dict_temp.keys() and der in GeneradorC3D.dict_temp.keys():
        #     GeneradorC3D.dict_temp[resultado] = self.operaciones(GeneradorC3D.dict_temp[izq], GeneradorC3D.dict_temp[der], ope)
        # elif izq in GeneradorC3D.dict_temp.keys():
        #     GeneradorC3D.dict_temp[resultado] = self.operaciones(GeneradorC3D.dict_temp[izq], float(der), ope)
        # elif der in GeneradorC3D.dict_temp.keys():
        #     GeneradorC3D.dict_temp[resultado] = self.operaciones(float(izq), GeneradorC3D.dict_temp[der], ope)
        # else:
        #     GeneradorC3D.dict_temp[resultado] = self.operaciones(float(izq), float(der), ope)
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
        self.agregarPrint('c', tempComp)
        self.agregarExp(tempH, tempH, '1', '+')
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