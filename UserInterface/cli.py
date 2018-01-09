from Validator.Validator import Validator


class CLI():
    count = 0
    def __init__(self, gameController, commandParser, validator):
        self.gameController = gameController
        self.commandParser = commandParser
        self.validator = validator

    def mainLoop(self):

        while True:
            #F3 0; C6 3: example of placed input

            self.commandParser.readCommand()
            command = self.commandParser.getCommand()
            params = self.commandParser.getParams()
            type = ""
            if command == "place":
                if len(params) == 0:
                    type = "placed"
                    # let the user pick the placement of the planes
                elif params[0] == "rand":
                    # place the user's planes randomly
                    type = "random"
                if type is not "":
                    self.gameController.play(type)  # start the game...
            elif command == "help":
                self.__printHelp()
            elif command == "exit":
                break
        return 0

    @staticmethod
    def getAttackInput():
        """
        :param self:
        :return: [col, row]
        """
        CLI.count += 1
        while True:
            try:
                coords = input("Coords of the target (ex: B5): ")
                # if int(coords) == -1:
                #    return [-1, -1, -1]
                if len(Validator.validateAttackInput(coords)) == 0:
                    if coords[0].islower():
                        x = ord(coords[0]) - ord('a')
                    if coords[0].isupper():
                        x = ord(coords[0]) - ord('A')

                    y = int(coords[1])
                    return [x, y-1]
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
                # if int(coords) == -1:
                #    return [-1, -1, -1]
                rot = int(input("Rotations to the left: "))
                if len(Validator.validateAttackInput(coords)) == 0:
                    if coords[0].islower():
                        x = ord(coords[0]) - ord('a')
                    if coords[0].isupper():
                        x = ord(coords[0]) - ord('A')

                    y = int(coords[1])
                    return [x, y-1, rot]
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

    def __printHelp(self):
        help = ""

        help += "Planes game against the PC\n"
        help += "Commands available:\n "
        help += "*place rand/placed*: Place a player's planes randomly or it lets the player select the placement of a plane\n" \
                "and its rotation\n E.g. place placed\n"
        help += "**The game will ask each player to input the placement of the planes and input the coordinates of the tile\n" \
                "that you wish to target.\n"
        help += "**2 matrices will be displayed: your board and your targeting image which show your hits and misses \n" \
                "(discovered tiles) on the enemy's board"
        print(help)
    @staticmethod
    def _showSeparator():
        print("==============================================================================")

    @staticmethod
    def printMatrix(matrix, size, title):
        """
        Prints a size*size matrix with columns marked with A-H, lines from 1-8
        :param matrix: a size*size matrix
        :param size: int
        :param title: string
        :return: None
        """
        print(title)
        print(CLI.count)
        output = "   "
        for i in range(size + 1):
            if i == 0:
                for l in range(size):
                    output += str(chr(65 + l) + " ")
            output += "\n"
            for j in range(size + 1):
                if j == 0 and i>0:
                    output += str(i) + "| "
                if i==0:
                    output+="--"
                if i>=1 and j>=1:
                    output += str(matrix[i - 1][j - 1][0]) + " "

        print(output)
        print("\n")

    @staticmethod
    def warn(string):
        print(string)
