from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class While(Instruction):

    def __init__(self, fila, columna,  condition: Expression, block) -> None:
        super().__init__(fila,columna)
        self.condition = condition
        self.block = block
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.condition.generator = self.generator
        
        newLabel = self.generator.newLabel()
        self.generator.addLabel(newLabel)
        environment.labelCont = newLabel#continue

        valueCondition = self.condition.compile(environment)

        if(valueCondition.type == typeExpression.BOOL):
            self.generator.addLabel(valueCondition.trueLabel)

            newEnv = Environment(environment, "Ciclo-While")
            newEnv.labelBrk = valueCondition.falseLabel
            newEnv.labelCont = newLabel
            for ins in self.block:
                ins.generator = self.generator
                ins.compile(newEnv)

            self.generator.addGoto(newLabel)
            self.generator.addLabel(valueCondition.falseLabel)
        else:
            objErrores.setNewError(Error("Error: algo salio mal en la Instruccion While", self.fila, self.columna, dt_string))   
            print("ERROR EN WHILE")
        