from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Cadena(Expression):

    def __init__(self, fila, columna, typeExpression:typeExpression, value:str) -> None:
        super().__init__(fila,columna)
        self.typeExpression=typeExpression
        self.value = value
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        newTemp = self.generator.newTemp()
        self.generator.addExpression(newTemp,'H','','')
        self.generator.addSetHeap('H', str(len(self.value)))
        self.generator.addNextHeap()
        for char in str(self.value):
            self.generator.addSetHeap('H',str(ord(char)))
            self.generator.addNextHeap()
        self.generator.addSetHeap('H','-1')
        self.generator.addNextHeap()
        self.generator.addExpression(newTemp,newTemp,'0.12837','+')
        
        return Value(newTemp,True,typeExpression.STRING)

