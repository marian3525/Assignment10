import random
import numpy
from Domain.Plane import Plane
from random import randint
from UserInterface.cli import CLI


class GameController():
    def __init__(self):
        # 0-unknown, 0-air, 1-frame 2-hit, 3-cockpit, 4-unknown,
        # the targeting grids are filled with -1's at the beginning and updated as tiles are discovered

        self.__tileCode = {"air":1, "frame":2, "hit":3, "cockpit":4, "unknown":0}
        self.__lut = {}  # dictionary: key=the plane uid; value = Plane object at that position
        self.__destroyedPlanes = []  # TODO saving the id of the dead planes in order to check if a hit is on such a plane
        self.__player1Matrix = self.__buildMatrix(8, self.__tileCode["air"])  # the matrix representing player 1's plane placement
        self.__player1Targeting = self.__buildMatrix(8,
                                                     self.__tileCode["unknown"])  # the matrix with the hits and misses of the first player
        self.__player2Matrix = self.__buildMatrix(8, self.__tileCode["air"])  # the matrix representing player 2's plane placement
        self.__player2Targeting = self.__buildMatrix(8,
                                                     self.__tileCode["unknown"])  # the matrix with the hits and misses of the second player

    def play(self, type):
        """
        Initialize the game, allow input from both players and manage the results
        :return: None
        """
        self.initBoards(type)  # place the planes on the 2 boards

        outcome = self.checkGameState()  # either "Player 1" or "Player 2" at this point, handle the victory
        # since the last shot WILL be fired by one of the players for sure, destroying the last tile, there can't
        # exist a DRAW situation, the game is finite
        player = False
        while outcome == "":
            player = not player
            if player:
                self.player1Turn() # TODO display the board and the targeting image for the player here
            else:
                self.player2Turn()
            outcome = self.checkGameState()

        if outcome == "Player 1":
            self.endGame("player1")
        elif outcome == "Player 2":
            self.endGame("player2")

    def initBoards(self, type):
        """
        Configure the boards for the players by placing planes according to the rules
        :param type: placed/random; how to human player will place the planes
        :return:
        """
        if type == "random":

            planesPlaced = 0
            success = False
            # try to place a plane until it finds a proper position
            while success is not True:
                self.clear(self.__player1Matrix)
                success = self.__placePlanesRandomly(self.__player1Matrix, planesPlaced)
        elif type == "placed":
            done = 1
            while done == 1:
                self.clear(self.__player1Matrix)
                done = self.__placePlanes(self.__player1Matrix)
        planesPlaced = 0
        success = False

        while success is not True:
            self.clear(self.__player2Matrix)
            success = self.__placePlanesRandomly(self.__player2Matrix, planesPlaced)

    def __placePlanesRandomly(self, destination, builtPlanes):
        """
        Builds 2 planes on the destination matrix, without overlapping or going outside the borders
        :param destination: blank matrix to be populated
        :return: None
        """
        maxTries = 10  # the number of tries after which the algorithm will give up trying to place a plane
        planesPlaced = builtPlanes
        tries = 0

        while planesPlaced < 2 and tries < maxTries:
            # update the lookup table
            # each plane needs a 5x5 matrix on the board
            # the matrices may overlap iff. the overlapping tiles are marked as 0's
            # the plane must entirely fit on the board

            # get an offset for the centre of the plane, the tile between the wings and the tail plane
            x = numpy.random.random_integers(2, 5)
            y = numpy.random.random_integers(2, 5)

            rotations = randint(0, 4)
            uid = self.getUID()  # assign this plane's tiles an uid
            plane = Plane(rotations, uid, self.__tileCode)
            # get a random number of rotations for the plane to be placed
            if self.planeFits(destination, x, y):
                self.__lut.update({uid: plane})
                self._insertPlane(destination, plane, x, y)
                planesPlaced += 1
            tries += 1

        if planesPlaced == 2:
            return True
        else:
            return False

    def __placePlanes(self, dest):
        """
        Let the player feed in coordinates and rotations for the 2 planes
        :param dest: destination matrix
        :return: 0 if successful
        """
        planesPlaced = 0
        while planesPlaced is not 2:
            input = CLI.getPlaceInput()
            if input == [-1, -1, -1]:
                return 1
            x = input[0]
            y = input[1]
            rotations = input[2]

            plane = Plane(rotations, self.getUID())

            if self.planeFits(dest, x, y):
                self._insertPlane(dest, plane, x, y)
                planesPlaced += 1
            else:
                CLI.warn("Does not fit! Try another:")

    def planeFits(self, dest, x, y):
        """
        (x,y) the coordinates of the single tile between the tail plane and the main wings
        The corners of the source image may be already filled since they won't be used
        :param dest: destination matrix
        :param x: int
        :param y: int
        :return: True if the no relevant overlapping occurs or the overlapped tiles are 0's or corners, False otherwise
        **tested, working as expected
        """
        if 2 <= y <= 5 and 2 <= x <= 5:  # make sure the plane does not go outside borders
            # if a space of 5*5 is found, return True. If anything other than 0's is found, return False
            for i in range(y - 2, y + 2 + 1):
                for j in range(x - 2, x + 2 + 1):
                    if not (i == y - 2 and (j == x - 2 or j == x + 2) or i == y + 2 and (j == x - 2 or j == x + 2)) and \
                            dest[i][j][0] != self.__tileCode["air"]:
                        # if it isn't in a corner and it is different from air, there is no space
                        return False
        else:
            return False
        return True

    def _insertPlane(self, destination, plane, x, y):
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

        image = plane.getImage()
        id = plane.getId()

        for i in range(startLine, endLine + 1):
            for j in range(startCol, endCol + 1):
                # indexes for the image: m = i-startLine; n = j-startCol
                # each tile stores the type of type and the belonging plane
                if not (i == y - 2 and (j == x - 2 or j == x + 2) or i == y + 2 and (j == x - 2 or j == x + 2)):
                    destination[i][j][0] = image[i - startLine][j - startCol][0]
                    destination[i][j][1] = id

    def __buildMatrix(self, size, elem):
        """
        :param size: The size of the matrix
        :return: A size*size matrix of pairs [tile-type, id_of_belonging_plane]
        """
        matrix = numpy.zeros((size, size, 2), dtype=int)
        for i in range(size):
            for j in range(size):
                matrix[i][j] = elem
        return matrix

    def clear(self, matrix):
        for i in range(8):
            for j in range(8):
                matrix[i][j][0] = self.__tileCode["air"]
                matrix[i][j][1] = 0

    def fire(self, player, x, y):
        """
        Shoots a tile on the other player's board and returns the type of tile that was hit
        :param player: True - player 1, False - player 2
        :param x: the targeted column
        :param y: the targeted row
        :return: the type of tile hit (0 - air, 1 - airframe, 2 - cockpit, 3-hit)
        """
        if player == True:  # player1
            if self.__player2Matrix[y][x] == self.__tileCode["cockpit"]:
                self.destroyPlane(x,
                                  y)  # mark the entire plane as hit and update player1's targeting grid marking the cockpit as hit
                self.__player1Targeting[y][x] = self.__tileCode["cockpit"]

            elif self.__isHitOnDestroyedPlane(x, y):
                self.__player1Targeting[y][x] = self.__tileCode["hit"]

            elif self.__isHitOnAirframe(x, y):
                self.__player1Targeting = self.__tileCode["hit"]

            elif self.__isHitOnAir(x, y):
                self.__player1Targeting[y][x] = self.__tileCode["air"]

        elif player == False:  # player2
            if self.__player1Matrix[y][x] == self.__tileCode["cockpit"]:
                self.destroyPlane(x, y)

            elif self.__isHitOnDestroyedPlane(x, y):
                self.__player2Targeting[y][x] = self.__tileCode["hit"]

            elif self.___isHitOnAirframe(x, y):
                self.__player2Targeting = self.__tileCode["hit"]

            elif self.__isHitOnAir(x, y):
                self.__player2Targeting[y][x] = self.__tileCode["air"]

    def player1Turn(self):
        # get player input from the UI and fire accordingly
        CLI.printMatrix(self.__player1Matrix, 8, "PLAYER 1 BOARD:")
        CLI.printMatrix(self.__player1Targeting, 8, "Target image:")
        coords = CLI.getAttackInput()

    def player2Turn(self):
        #TODO ~player1, do not display the matrices as the player should not see the board of the opponent (PC)
        pass

    def checkGameState(self):
        """
        :return: string: The name of the winning player or an empty string if the game can continue
        """
        player1Check = False
        player2Check = False

        for i in range(8):
            for j in range(8):
                if self.__player1Matrix[i][j][0] in [1, 2]:
                    player1Check = True # player 1 may continue, not all tiles are hit

                if self.__player2Matrix[i][j][0] in [1, 2]:
                    player2Check = True # player 2 may continue, not all tiles are hit

        if player2Check and player1Check:
            return "" # both players may continue, no winner yet

        elif player1Check is False:
            return "Player 2"  # player 2 won
        elif player2Check is False:
            return "Player 1"  # player 1 won

    def endGame(self, winner):
        if winner == "player1":
            CLI.warn("Player 1 won!")
        else:
            CLI.warn("Player 2 won!")

    def getUID(self):
        """
        Generate a unique ID which is not already in the look up table
        :return: int
        """
        uid = randint(1, 9999)
        while uid in self.__lut.values():
            uid = randint(1, 9999)
        return uid

    def __isHitOnDestroyedPlane(self, matrix, x, y):
        """
        :param x: int
        :param y: int
        :return: True if (y,x) is a tile on a plane entirely marked with 1's, False otherwise
        """
        id = matrix[y][x][1]
        alive = [self.__tileCode["fame"], self.__tileCode["cockpit"]]

        for i in range(8):
            for j in range(8):
                if matrix[i][j][1] == id and matrix[i][j][0] in alive:
                    return True
        return False

    def __isHitOnAirframe(self, matrix, x, y):
        """

        :param x: int
        :param y: int
        :return: True if (y,x) tile is marked with a 1
        """
        return matrix[y][x][0] == self.__tileCode["frame"]

    def __isHitOnAir(self, matrix, x, y):
        """

        :param x: int
        :param y: int
        :return: True if (y,x) tile is marked with a 1
        """
        return matrix[y][x][0] == self.__tileCode["air"]

    def __isHitOnCockpit(self, matrix, x, y):
        return matrix[y][x][0] == self.__tileCode["cockpit"]

