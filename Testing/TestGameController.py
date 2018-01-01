import unittest

import numpy
from Controller.GameController import GameController
from Domain.Plane import Plane


class TestGameController(unittest.TestCase):
    def setUp(self):
        self.gc = GameController()
        self.testMatrix = self.buildMatrix(8, 0)

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

    def testPlaneFits(self):
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

        self.testMatrix[3][4][0] = 1
        self.testMatrix[5][2][0] = 1

        self.assertFalse(self.gc.planeFits(self.testMatrix, 0, 0))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 1, 1))

        self.assertFalse(self.gc.planeFits(self.testMatrix, 3, 4))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 2, 3))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 3, 5))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 4, 4))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 2, 2))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 3, 2))

        self.testMatrix[3][4][0] = 0

        self.assertFalse(self.gc.planeFits(self.testMatrix, 2, 5))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 2, 3))

    def testInsertPlane(self):
        plane = Plane(0, 0)

        testDestination = self.buildMatrix(8, 0)

        self.gc._insertPlane(testDestination, plane, 2, 2)
        plane = Plane(1, 1)
        self.gc._insertPlane(testDestination, plane, 5, 5)

        self.debugPrint(testDestination, 8)

        self.assertEqual(testDestination[2][2][0], 1)
        self.assertEqual(testDestination[0][2][0], 2)
        self.assertEqual(testDestination[0][2][1], 0)
        self.assertEqual(testDestination[5][3][0], 2)
        self.assertEqual(testDestination[5][3][1], 1)
        self.assertEqual(testDestination[7][4][0], 1)
        self.assertEqual(testDestination[0][0][0], 0)
        self.assertEqual(testDestination[3][5][0], 0)

    def debugPrint(self, matrix, size):
        output = ""
        for i in range(size):
            for j in range(size):
                output += str(matrix[i][j][0]) + " "
            output += "\n"
        print(output)