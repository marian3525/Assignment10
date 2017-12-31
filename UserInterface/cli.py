class CLI():
    def __init__(self, gameController, commandParser, validator):
        self.gameController = gameController
        self.commandParser = commandParser
        self.validator = validator

    def mainLoop(self):
        player = True

        while True:
            if player==True:
                print("Player 1:")
            else:
                print("Player 2:")

            self.commandParser.readCommand()
            command = self.commandParser.getCommand()
            params = self.commandParser.getParams()

            if command == "fire":
                params = params[0]
                errorString = self.validator.validateAttackInput(params)
                if len(errorString) is 0:
                    if params[0].islower():
                        x = ord(params[0]) - ord('a')
                    if params[0].isupper():
                        x = ord(params[0]) - ord('A')

                    y = int(params[1])

                    self.gameController.fire(player, x, y)
                else:
                    print(errorString)

    def buildMatrix(self, size):
        """
        :param size: The size of the matrix
        :return: A size*size matrix of zeroes
        """
        matrix = [[0] * size for i in range(10)]
        return matrix

    def printMatrix(self, matrix, size):
        """
        Prints a size*size matrix
        :param matrix: a size*size matrix
        :param size: int
        :return: None
        """
        output = ""
        for i in range(size):
            for j in range(size):
                output += str(matrix[i][j]) + " "
            output += "\n"
        print(output)