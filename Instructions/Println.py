from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Println(Instruction):

    def __init__(self, fila, columna,  exp: Expression) -> None:
        super().__init__(fila,columna)
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.exp.generator = self.generator
        
        tempValue: Value = self.exp.compile(environment)

        if(tempValue != None):
            if(tempValue.type == typeExpression.INT):
                self.generator.addPrintf("d",str(tempValue.getValue()))

            elif(tempValue.type == typeExpression.FLOAT):
                self.generator.addPrintf("d",str(tempValue.getValue()))

            elif(tempValue.type == typeExpression.BOOL):
                newLabel = self.generator.newLabel()
                self.generator.addLabel(tempValue.trueLabel)
                self.generator.addCallFunc("print_true_proc")

                self.generator.addGoto(newLabel)
                self.generator.addLabel(tempValue.falseLabel)
                self.generator.addCallFunc("print_false_proc")

                self.generator.addLabel(newLabel)

            elif(tempValue.type==typeExpression.STRING):
                self.generator.addPrintStr()
                newTemp = self.generator.newTemp()
                self.generator.addExpression(newTemp,'P',str(environment.size),'+')
                self.generator.addExpression(newTemp,newTemp,'1','+')
                self.generator.addSetStack(newTemp,tempValue.value)
                self.generator.addNextStack(str(environment.size))
                self.generator.addCallFunc("print_string")
                temp = self.generator.newTemp()
                self.generator.addGetStack(temp,'P')
                self.generator.addBackStack(str(environment.size))

            else:
                objErrores.setNewError(Error("Error: algo salio mal en la Instruccion Println", self.fila, self.columna, dt_string))   
                print("Error en print")

            self.generator.addNewLine()

    