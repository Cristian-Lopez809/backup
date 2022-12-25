from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Len(Instruction):
    def __init__(self, fila, columna, exp: Expression) -> None:
        super().__init__(fila,columna)
        self.exp = exp
        self.fila = fila
        self.columna = columna
    
    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.exp.generator = self.generator
        #agregar arrays
        expresion = self.exp.compile(environment)
        if expresion is None:
            objErrores.setNewError(Error("Error: Error en la Instruccion Len", self.fila, self.columna, dt_string))   
            print('Error con el arreglo')
            return
        newTemp =  self.generator.newTemp()
        self.generator.addExpression(newTemp, expresion.value, '', '')
        self.generator.addGetHeap(newTemp,newTemp)
        return Value(newTemp,True,typeExpression.INT)
