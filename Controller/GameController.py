import random

from Domain.Plane import Plane
from random import randint


class GameController():
    def __init__(self):
        # 0-air, 1-airframe, 2-cockpit, 3-hit
        # the targeting grids are filled with -1's at the beginning and updated as tiles are discovered
        self.__lut = {}  # dictionary: key=the plane uid; value = Plane object at that position
        self.__destroyedPlanes = []  # saving the id of the dead planes in order to check if a hit is on such a plane
        self.__player1Matrix = self.__buildMatrix(8, 0)  # the matrix representing player 1's plane placement
        self.__player1Targeting = self.__buildMatrix(8,
                                                     -1)  # the matrix with the hits and misses of the first player
        self.__player2Matrix = self.__buildMatrix(8, 0)  # the matrix representing player 2's plane placement
        self.__player2Targeting = self.__buildMatrix(8,
                                                     -1)  # the matrix with the hits and misses of the second player

    def play(self):
        """
        Initialize the game, allow input from both players and manage the results
        :return: None
        """
        self.initBoards()

        while self.checkGameState() == "":  # The main game loop
            pass

        outcome = self.checkGameState()  # eiter "Player 1" or "Player 2" at this point, handle the victory
        # since the last shot WILL be fired by one of the players for sure, destroying the last tile, there can't
        # exist a DRAW situation, the game is finite
        return outcome

    def initBoards(self):
        """
        Configure the boards for the players by placing planes according to the rules
        :return:
        """
        # try to place a plane until it find a proper position
        while self.__placePlanes(self.__player1Matrix) == 0:
            continue

        while self.__placePlanes(self.__player2Matrix) == 0:
            continue

    def __placePlanes(self, destination):
        """
        Builds 2 planes on the destination matrix, without overlapping or going outside the borders
        :param destination: blank matrix to be populated
        :return: None
        """
        maxTries = 50  # the number of tries after which the algorithm will give up trying to place a plane
        planesPlaced = 0
        tries = 0

        while planesPlaced < 2 and tries < maxTries:
            # update the lookup table
            # each plane needs a 5x5 matrix on the board
            # the matrices may overlap iff. the overlapping tiles are marked as 0's
            # the plane must entirely fit on the board

            # get an offset for the centre of the plane, the tile between the wings and the tail plane
            x = randint(0, 5)
            y = randint(0, 5)
            # get a random number of rotations for the plane to be placed
            rotations = randint(0, 5)

            uid = self.getUID()  # assign this plane's tiles an uid
            plane = Plane(rotations, uid)

            if self.planeFits(destination, x, y):
                self.__lut.update({uid: plane})
                self.__insertPlane(self.__player1Matrix, plane, x, y)
                planesPlaced += 1
            tries += 1

        if tries < maxTries:
            return 0  # Success
        else:
            return tries  # Failed to find a place to insert a plane

    def planeFits(self, dest, x, y):
        """
        (x,y) the coordinates of the single tile between the tail plane and the main wings
        The corners of the source image may be already filled since they won't be used
        :param dest: destination matrix
        :param x: int
        :param y: int
        :return: True if the no relevant overlapping occurs or the overlapped tiles are 0's or corners, False otherwise
        """
        if 2 <= y <= 5 and 2 <= x <= 5:  # make sure the plane does not go outside borders
            # if a space of 5*5 is found, return True. If anything other than 0's is found, return False
            for i in range(y - 2, y + 2 + 1):
                for j in range(x - 2, x + 2 + 1):
                    if not (i == y - 2 and (j == x - 2 or j == x + 2) or i == y + 2 and (j == x - 2 or j == x + 2)) and dest[i][j][0] != 0:
                        # if it isn't in a corner and it is different from 0, there is no space
                        return False
        else:
            return False
        return True

    def __insertPlane(self, destination, plane, x, y):
        """
        Places a plane with the center at x,y
        :param destination: the destination matrix
        :param plane: the plane to be placed
        :param x: target column
        :param y: target row
        :return: None
        """
        startLine = y - 2
        endLine = y + 2
        startCol = x - 2
        endCol = x + 2

    def __buildMatrix(self, size, elem):
        """
        *by building the matrix with [elem*size for i in range(size)]
        :param size: The size of the matrix
        :return: A size*size matrix of pairs [tile-type, id_of_belonging_plane]
        """
        matrix = [elem for i in range(2)]
        matrix = [matrix for i in range(size)]
        matrix = [matrix for i in range(size)]
        return matrix

    def fire(self, player, x, y):
        """
        Shoots a tile on the other player's board and returns the type of tile that was hit
        :param player: True - player 1, False - player 2
        :param x: the targeted column
        :param y: the targeted row
        :return: the type of tile hit (0 - air, 1 - airframe, 2 - cockpit, 3-hit)
        """
        if player == True:  # player1
            if self.__player2Matrix[y][x] == 2:
                self.destroyPlane(x,
                                  y)  # mark the entire plane as hit and update player1's targeting grid marking the cockpit as hit

            elif self.__isHitOnDestroyedPlane(x, y):
                self.__player1Targeting[y][x] = 1

            elif self.__isHitOnAirframe(x, y):
                self.__player1Targeting = 1

            elif self.__isHitOnAir(x, y):
                self.__player1Targeting[y][x] = 0

        elif player == False:  # player2
            if self.__player1Matrix[y][x] == 2:
                self.destroyPlane(x, y)

            elif self.__isHitOnDestroyedPlane(x, y):
                self.__player2Targeting[y][x] = 1

            elif self.___isHitOnAirframe(x, y):
                self.__player2Targeting = 1

            elif self.__isHitOnAir(x, y):
                self.__player2Targeting[y][x] = 0

    def player1Turn(self):
        pass

    def player2Turn(self):
        pass

    def checkGameState(self):
        """
        :return: string: The name of the winning player or an empty string if the game can continue
        """
        player1Check = False
        player2Check = False

        for i in range(8):
            for j in range(8):
                if self.__player1Matrix[i][j] not in [0,
                                                      3]:  # if there are alive tiles, mark the player as one who can continue
                    player1Check = True

                if self.__player2Matrix[i][j] not in [0, 3]:
                    player2Check = True

        if player2Check and player1Check:
            return ""

        elif player1Check is False:
            return "Player 2"  # player 2 won
        elif player2Check is False:
            return "Player 1"  # player 1 won

    def getUID(self):
        """
        Generate a unique ID which is not already in the look up table
        :return: int
        """
        uid = randint(9999)
        while uid in self.__lut.values():
            uid = randint(9999)
        return uid

    def __isHitOnDestroyedPlane(self, matrix, x, y):
        """
        :param x: int
        :param y: int
        :return: True if (y,x) is a tile on a plane entirely marked with 1's, False otherwise
        """
        return matrix[y][x][0] == 7  # TODO scan the board for tiles with the id of the plane

    def __isHitOnAirframe(self, matrix, x, y):
        """

        :param x: int
        :param y: int
        :return: True if (y,x) tile is marked with a 1
        """
        return matrix[y][x][0] == 1

    def __isHitOnAir(self, matrix, x, y):
        """

        :param x: int
        :param y: int
        :return: True if (y,x) tile is marked with a 1
        """
        return matrix[y][x][0] == 0

    def __isHitOnCockpit(self, matrix, x, y):
        return matrix[y][x][0] == 2

    def debugPrint(self, matrix, size):
        output = ""
        for i in range(size):
            for j in range(size):
                output += str(matrix[i][j][0]) + " "
            output += "\n"
        print(output)

    def debug(self):
        # Method to be called from the appstart in order to debug the inner code
        pass
