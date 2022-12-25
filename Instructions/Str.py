from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Expression.Primitive.Cadena import Cadena

class Str(Instruction):
    def __init__(self, fila, columna, exp: Expression) -> None:
        super().__init__(fila, columna)
        self.exp = exp
        self.fila = fila
        self.columna = columna
    
    def compile(self, environment: Environment) -> Value:
        self.exp.generator = self.generator
        #agregar arrays
        expresion = self.exp.compile(environment)
        if expresion is None:
            print('Error con el arreglo')
            return
        prueba  = Cadena(self.fila,self.columna,typeExpression.STRING,str(expresion.value))
        print(prueba.value)
        newTemp = self.generator.newTemp()
        self.generator.addExpression(newTemp,'H','','')
        self.generator.addSetHeap('H', str(len(prueba.value)))
        self.generator.addNextHeap()
        for char in str(prueba.value):
            self.generator.addSetHeap('H',str(ord(char)))
            self.generator.addNextHeap()
        self.generator.addSetHeap('H','-1')
        self.generator.addNextHeap()
        self.generator.addExpression(newTemp,newTemp,'0.12837','+')
        
        return Value(newTemp,True,typeExpression.STRING)