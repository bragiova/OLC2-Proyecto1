
from Sym.Error import Error
from Sym.Simbolo import Simbolo

class TablaSimbolos:
    errores = []
    variables = {}
    funciones = {}

    def __init__(self, envAnterior = None):
        self.tablaS = {}
        self.tablaF = {}
        self.envAnterior = envAnterior
        self.size = 0
        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''
        if envAnterior is not None:
            self.size = self.envAnterior.size
            self.breakLbl = self.envAnterior.breakLbl
            self.continueLbl = self.envAnterior.continueLbl
            self.returnLbl = self.returnLbl
    
    # Se guardan las variables en la tabla de símbolos
    def guardarVar(self, ident, tipo, enHeap, linea, columna, find = True):
        if find:
            envActual = self
            while envActual != None:
                if ident in envActual.tablaS:
                    envActual.tablaS[ident] = Simbolo(ident, tipo, envActual.envAnterior == None, envActual.tablaS[ident].getPosicion(), enHeap, linea, columna)
                    TablaSimbolos.variables[ident] = envActual.tablaS[ident]
                    return envActual.tablaS[ident]
                else:
                    envActual = envActual.envAnterior
        
        if ident in self.tablaS:
            self.tablaS[ident] = Simbolo(ident, tipo, self.envAnterior == None, self.tablaS[ident].getPosicion(), enHeap, linea, columna)
            TablaSimbolos.variables[ident] = self.tablaS[ident]
            return self.tablaS[ident]
        else:
            nuevoSimb = Simbolo(ident, tipo, self.envAnterior == None, self.size, enHeap, linea, columna)
            self.size += 1
            self.tablaS[ident] = nuevoSimb
            TablaSimbolos.variables[ident] = self.tablaS[ident]
            return self.tablaS[ident]

    # Se guardan las funciones en la tabla de símbolos
    def guardarFuncion(self, ident, objFuncion):
        # Se recibirá un objeto de tipo Función
        self.tablaF[ident] = objFuncion
        TablaSimbolos.funciones[ident] = objFuncion

    # Se obtiene un símbolo almacenado en la tabla de símbolos
    def getSimbolo(self, id):
        envActual = self
        while envActual != None:
            if id in envActual.tablaS:
                return envActual.tablaS[id]
            envActual = envActual.envAnterior
        return None
    
    def getFuncion(self, ident):
        entorno = self
        while entorno != None:
            if ident in entorno.tablaF:
                return entorno.tablaF[ident]
            entorno = entorno.envAnterior
        return None
    
    # Se actualiza el valor de un símbolo en la tabla de símbolos
    def updateTabla(self, ident, tipo, enHeap, linea, columna):
        envActual = self
        while envActual != None:
            if ident in envActual.tablaS:
                envActual.tablaS[ident].setTipo(tipo)
                TablaSimbolos.variables[ident].setEnHeap(enHeap)
                return envActual.tablaS[ident]
            else:
                envActual = envActual.envAnterior
        
        if ident in self.tablaS:
            self.tablaS[ident] = Simbolo(ident, tipo, self.envAnterior == None, self.tablaS[ident].getPosicion(), enHeap, linea, columna)
            TablaSimbolos.variables[ident] = self.tablaS[ident]
            return self.tablaS[ident]
        # return Error("Semántico", "Variable no encontrada", -1, -1)
    
    def existeSimbEnActual(self,identificador):
        entorno = self
        existe = entorno.tablaS.get(identificador)
        if existe is not None:
            return True
        else:
            return False
        
    def getEntornoGlobal(self):
        entorno = self
        while entorno.envAnterior is not None:
            entorno = entorno.envAnterior
        return entorno

