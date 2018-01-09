import unittest

import numpy
from Controller.GameController import GameController
from Domain.Plane import Plane


class TestGameController(unittest.TestCase):
    def setUp(self):
        self.gc = GameController()
        self.testMatrix = self.buildMatrix(8, 0)
        self.__tileCode = {"air": 1, "frame": 2, "hit": 3, "cockpit": 4, "unknown": 0}

    def buildMatrix(self, size, elem):
        """
        :param size: The size of the matrix
        :return: A size*size matrix of zeroes
        """
        matrix = numpy.zeros((size, size, 2), dtype=int, order='C')
        for i in range(size):
            for j in range(size):
                matrix[i][j] = elem
        return matrix

    def testPlaneFits(self):
        self.testMatrix = self.buildMatrix(8, self.__tileCode["air"])
        self.assertFalse(self.gc.planeFits(self.testMatrix, 0, 0))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 1, 1))

        self.assertTrue(self.gc.planeFits(self.testMatrix, 2, 2))
        self.assertTrue(self.gc.planeFits(self.testMatrix, 3, 3))
        self.assertTrue(self.gc.planeFits(self.testMatrix, 4, 4))
        self.assertTrue(self.gc.planeFits(self.testMatrix, 5, 5))

        self.assertFalse(self.gc.planeFits(self.testMatrix, 6, 7))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 7, 7))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 3, 6))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 0, 5))

        self.testMatrix[3][4][0] = self.__tileCode["frame"]
        self.testMatrix[5][2][0] = self.__tileCode["frame"]

        self.assertFalse(self.gc.planeFits(self.testMatrix, 0, 0))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 1, 1))

        self.assertFalse(self.gc.planeFits(self.testMatrix, 3, 4))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 2, 3))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 3, 5))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 4, 4))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 2, 2))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 3, 2))

        self.testMatrix[3][4][0] = self.__tileCode["air"]

        self.assertFalse(self.gc.planeFits(self.testMatrix, 2, 5))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 2, 3))

    def testInsertPlane(self):
        plane = Plane(0, 0, self.__tileCode)

        testDestination = self.buildMatrix(8, self.__tileCode["air"])

        self.gc._insertPlane(testDestination, plane, 2, 2)
        plane = Plane(1, 1, self.__tileCode)
        self.gc._insertPlane(testDestination, plane, 5, 5)

        self.debugPrint(testDestination, 8)

        self.assertEqual(testDestination[2][2][0], self.__tileCode["frame"])
        self.assertEqual(testDestination[0][2][0], self.__tileCode["cockpit"])
        self.assertEqual(testDestination[5][3][0], self.__tileCode["cockpit"])
        self.assertEqual(testDestination[3][4][0], self.__tileCode["frame"])
        self.assertEqual(testDestination[7][4][0], self.__tileCode["frame"])
        self.assertEqual(testDestination[0][0][0], self.__tileCode["air"])
        self.assertEqual(testDestination[3][5][0], self.__tileCode["air"])

    def debugPrint(self, matrix, size):
        print("DEBUG")
        output = "   "
        for i in range(size + 1):
            if i == 0:
                for l in range(size):
                    output += str(chr(65 + l) + " ")
            output += "\n"
            for j in range(size + 1):
                if j == 0 and i > 0:
                    output += str(i) + "| "
                if i == 0:
                    output += "--"
                if i >= 1 and j >= 1:
                    output += str(matrix[i - 1][j - 1][0]) + " "

        print(output)
        print("\n")
