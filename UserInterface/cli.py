
from Validator.Validator import Validator


class CLI():
    def __init__(self, gameController, commandParser, validator):
        self.gameController = gameController
        self.commandParser = commandParser
        self.validator = validator

    def mainLoop(self):
        player = True

        while True:
            if player == True:
                print("Player 1:")
            else:
                print("Player 2:")

            self.commandParser.readCommand()
            command = self.commandParser.getCommand()
            params = self.commandParser.getParams()

            if command == "place":
                if len(params) == 0:
                    type = "placed"
                    # let the user pick the placement of the planes
                elif params[0] == "rand":
                    # place the user's planes randomly
                    type = "random"

                self.gameController.play(type) # start the game...
            elif command == "exit":
                break
        return 0

    @staticmethod
    def getAttackInput(self):
        while True:
            try:
                coords = input("Coords of the target (ex: B5): ")
                #if int(coords) == -1:
                #    return [-1, -1, -1]
                if len(Validator.validateAttackInput(coords)) == 0:
                    if coords[0].islower():
                        x = ord(coords[0]) - ord('a')
                    if coords[0].isupper():
                        x = ord(coords[0]) - ord('A')

                    y = int(coords[1])
                    return [x, y]
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input! Try again or -1 to exit")
                continue
    @staticmethod
    def getPlaceInput():
        """
        Read the coords of the plane and its rotation
        :return: [x,y,rotations] of the plane to be placed or [-1,-1,-1] if the op. was not successful
        """
        while True:
            try:
                coords = input("Coords of the plane (ex: B5): ")
                #if int(coords) == -1:
                #    return [-1, -1, -1]
                rot = int(input("Rotations to the left: "))
                if len(Validator.validateAttackInput(coords)) == 0:
                    if coords[0].islower():
                        x = ord(coords[0]) - ord('a')
                    if coords[0].isupper():
                        x = ord(coords[0]) - ord('A')

                    y = int(coords[1])
                    return [x, y, rot]
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input! Try again or -1 to exit")
                continue

    def buildMatrix(self, size):
        """
        :param size: The size of the matrix
        :return: A size*size matrix of zeroes
        """
        matrix = [[0] * size for i in range(10)]
        return matrix
    @staticmethod
    def printMatrix(matrix, size):
        """
        Prints a size*size matrix
        :param matrix: a size*size matrix
        :param size: int
        :return: None
        """
        output = ""
        for i in range(size):
            for j in range(size):
                output += str(matrix[i][j][0]) + " "
            output += "\n"
        print(output)

    @staticmethod
    def warn(string):
        print(string)
