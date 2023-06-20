
from Sym.Error import Error

class TablaSimbolos:
    errores = []
    variables = {}
    funciones = {}

    def __init__(self, envAnterior = None):
        self.tablaS = {}
        self.tablaF = {}
        self.envAnterior = envAnterior
    
    # Se guardan las variables en la tabla de símbolos
    def guardarVar(self, simbolo):
        self.tablaS[simbolo.getId()] = simbolo
        TablaSimbolos.variables[simbolo.getId()] = simbolo

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
    def updateTabla(self, simbolo):
        envActual = self
        while envActual != None:
            if simbolo.getId() in envActual.tablaS:
                envActual.tablaS[simbolo.getId()].setValor(simbolo.getValor())
                TablaSimbolos.variables[simbolo.getId()] = simbolo
                return None
            else:
                envActual = envActual.envAnterior
        return Error("Semántico", "Variable no encontrada", simbolo.getLinea(), simbolo.getColumna())
    
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

