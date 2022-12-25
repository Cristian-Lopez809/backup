from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Upper(Instruction):

    def __init__(self, fila, columna, exp: Expression) -> None:
        super().__init__(fila,columna)
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        self.exp.generator=self.generator
        cadena = self.exp.compile(environment)
        self.generator.addToUpper()
        newTemp = self.generator.newTemp()
        self.generator.addExpression(newTemp,'P',str(environment.size),'+')
        self.generator.addExpression(newTemp,newTemp,'1','+')
        self.generator.addSetStack(newTemp,cadena.value)
        #newEnv = Environment(environment)
        #self.generator(newEnv)
        self.generator.addCallFunc("to_upper")
        temp1=self.generator.newTemp()
        temp2=self.generator.newTemp()
        self.generator.addExpression(temp2,'P','1','+')
        self.generator.addGetStack(temp1,'int('+temp2+')')
        return Value(temp1,True,typeExpression.STRING)

        
    