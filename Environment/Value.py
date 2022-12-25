from Enum.typeExpression import typeExpression

class Value:
    def __init__(self,value:str, isTemp:bool, type: typeExpression) -> None:
        self.value = value
        self.isTemp = isTemp
        self.type = type
        self.trueLabel = ""
        self.falseLabel = ""
        self.struct_type = ""

    def getValue(self) -> str:
        return self.value