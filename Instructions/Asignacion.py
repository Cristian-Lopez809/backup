from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Asignacion(Instruction):

    def __init__(self, fila, columna,  id:str, exp: Expression) -> None:
        super().__init__(fila,columna)
        self.id = id
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.exp.generator = self.generator
        
        newValue: Value = self.exp.compile(environment)
        oldVar: Symbol = environment.getVariable(self.id)

        if oldVar != None:
            if(oldVar.type != typeExpression.UNDEFINED):

                if(oldVar.type == newValue.type):
                    print("Match Type")
                    if(oldVar.type != typeExpression.BOOL):
                        self.generator.addSetStack(str(oldVar.position),newValue.getValue())
                    else:
                        newLabel = self.generator.newLabel()
                        self.generator.addLabel(newValue.trueLabel)
                        self.generator.addSetStack(str(oldVar.position),'1')
                        self.generator.addGoto(newLabel)
                        self.generator.addLabel(newValue.falseLabel)
                        self.generator.addSetStack(str(oldVar.position),'0')
                        self.generator.addGoto(newLabel)
                        self.generator.addLabel(newLabel)
                else:
                    objErrores.setNewError(Error("Error: el tipo de dato no coincide con el especificado", self.fila, self.columna, dt_string))   
                    print("Error: no hizo match con los tipos")
            else:#asignacion de var pre-declarada
                oldVar.setType(newValue.type)
                self.generator.addSetStack(str(oldVar.position), str(newValue.getValue()))
        else:
            objErrores.setNewError(Error("Error: la variable a asignar no existe", self.fila, self.columna, dt_string))   
            print("Error: La variable a asignar no existe")
