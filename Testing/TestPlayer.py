import unittest

import numpy
from Autoplayer.Player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.__tileCode = {"air": 1, "frame": 2, "hit": 3, "cockpit": 4, "unknown": 0}

    def tearDown(self):
        pass

    def testFindCabin1(self):
        img = self.getTargetImage1()
        player = Player(img)

        self.assertEqual(player.nextMove(), [5,4]) # (j, i-1)

    def testFindCabin2(self):
        img = self.getTargetImage2()
        player = Player(img)

        self.assertEqual(player.nextMove(), [4,5]) # (j-1, i)

    def testFindCabin3(self):
        img = self.getTargetImage3()
        player = Player(img)

        self.assertEqual(player.nextMove(), [5, 6]) # (j, i+1)

    def testFindCabin4(self):
        img = self.getTargetImage4()
        player = Player(img)

        self.assertEqual(player.nextMove(), [6, 5]) # (j+1, I)


    def getTargetImage1(self):
        img = self.buildMatrix(8, -1)
        # simulate the first branch in the Autoplayer
        img[5][5] = 1
        img[5][4] = 1
        img[5][6] = 1
        img[6][5] = 1
        return img

    def getTargetImage2(self):
        img = self.buildMatrix(8, self.__tileCode["unknown"])
        # second branch
        img[5][5] = self.__tileCode["frame"]
        img[4][5] = self.__tileCode["frame"]
        img[6][5] = self.__tileCode["frame"]
        img[5][6] = self.__tileCode["frame"]
        return img

    def getTargetImage3(self):
        img = self.buildMatrix(8, self.__tileCode["unknown"])
        # third branch
        img[5][5] = self.__tileCode["frame"]
        img[5][4] = self.__tileCode["frame"]
        img[5][6] = self.__tileCode["frame"]
        img[4][5] = self.__tileCode["frame"]
        return img

    def getTargetImage4(self):
        img = self.buildMatrix(8, self.__tileCode["unknown"])
        # last branch
        img[5][5] = self.__tileCode["frame"]
        img[5][4] = self.__tileCode["frame"]
        img[4][5] = self.__tileCode["frame"]
        img[6][5] = self.__tileCode["frame"]
        return img

    def buildMatrix(self, size, elem):
        """
        :param size: The size of the matrix
        :return: A size*size matrix of zeroes
        """
        matrix = numpy.zeros((size, size, 2), dtype=int)
        for i in range(size):
            for j in range(size):
                matrix[i][j] = elem
        return matrix
