from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Break(Instruction):

    def __init__(self,  fila, columna ) -> None:
        super().__init__(fila,columna)
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        if environment.labelBrk == '':
            objErrores.setNewError(Error("Error: break fuera de cilo ", self.fila, self.columna, dt_string))   
            print('break fuera de ciclo')
            return
        
        self.generator.addGoto(environment.labelBrk)