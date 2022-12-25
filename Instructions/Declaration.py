from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Environment.SymbolsTable import SymbolsTable
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Declaration(Instruction):

    def __init__(self, fila, columna,  id:str, exp: Expression, type:typeExpression) -> None:
        super().__init__(fila,columna)
        self.id = id
        self.exp = exp
        self.type = type
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.exp.generator = self.generator
        
        newValue: Value = self.exp.compile(environment)

        if newValue != None:
            tempVar: Symbol = environment.saveVariable(self.id,self.type, self.fila, self.columna,(newValue.type == typeExpression.STRING or newValue.type == typeExpression.STRUCT or newValue.type == typeExpression.INT), newValue.struct_type)
            tmpTabla = SymbolsTable()
            tmpTabla.setNewSimbol(tempVar)

            if(self.type != typeExpression.BOOL):
                self.generator.addSetStack(str(tempVar.position),newValue.getValue())
            else:
                newLabel = self.generator.newLabel()
                if(newValue.trueLabel != ""):
                    self.generator.addSetStack(str(tempVar.position),'1')
                elif(newValue.falseLabel != ""):
                    self.generator.addSetStack(str(tempVar.position),'0')
                else:
                    print("Me dio ansiedad la declaracion de Booleano")
                self.generator.addGoto(newLabel)
                self.generator.addLabel(newLabel)
        else:
            objErrores.setNewError(Error("Error: expresion de tipo None en la Declaracion", self.fila, self.columna, dt_string))   
            print("Error, expresion de tipo None en declaracion")
