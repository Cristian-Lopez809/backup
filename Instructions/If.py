from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class If(Instruction):

    def __init__(self, fila, columna,  condition: Expression, block, blockElse, blockElseIf) -> None:
        super().__init__(fila,columna)
        self.condition = condition
        self.block = block
        self.blockElse = blockElse
        self.blockElseIf = blockElseIf
        self.gotoTrue = None
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.condition.generator = self.generator
        

        valueCondition = self.condition.compile(environment)
        escapeLabel = self.generator.newLabel()   

        if(valueCondition.type == typeExpression.BOOL):
            self.generator.addLabel(valueCondition.trueLabel)

            newEnv = Environment(environment, "Condicional-If")
            for ins in self.block:
                ins.generator = self.generator
                ins.compile(newEnv)
            
            temp = self.generator.label
            self.generator.addGoto(escapeLabel)
            if self.blockElse != None:
                self.generator.addLabel(valueCondition.falseLabel)
                newEnv = Environment(environment, "Condicional-If")
                for ins in self.blockElse:
                    ins.generator = self.generator
                    ins.compile(newEnv)
                
            elif self.blockElseIf != None:
                self.generator.addLabel(valueCondition.falseLabel)
                newEnv = Environment(environment, "Condicional-If")
                self.blockElseIf.generator = self.generator
                self.blockElseIf.compile(newEnv)
                self.generator.addGoto(escapeLabel)
                #newLabelElse = self.generator.newLabel()
                #self.generator.addLabel(newLabelElse)
            else:
                self.generator.addLabel(valueCondition.falseLabel)
            
            self.generator.addLabel(escapeLabel)
                
        else:
            objErrores.setNewError(Error("Error: Error en el Ciclo If", self.fila, self.columna, dt_string))   
            print("ERROR EN IF")
        