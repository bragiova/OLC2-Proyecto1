
class Error:
    def __init__(self, tipoError, desc, linea, columna):
        self.tipoError = tipoError
        self.desc = desc
        self.linea = linea
        self.columna = columna
    
    def getError(self):
        return self.tipo + ' - ' + self.desc + ' {' + str(self.linea) + ', ' + str(self.columna) + '};'
