class Validator():
    def __init__(self):
        pass
    @staticmethod
    def validateAttackInput(inputString):
        errorString = ""
        if len(inputString) == 0 or len(inputString) > 2:
            errorString += "Invalid params!"

        if not inputString[1].isdigit():
            errorString += "Invalid column"

        if not inputString[0].isalpha():
            errorString += "Invalid row"

        return errorString
