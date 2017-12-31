import unittest

from Controller.GameController import GameController


class TestGameController(unittest.TestCase):
    def setUp(self):
        self.gc = GameController()
        self.testMatrix=self.buildMatrix(8, 0)

    def buildMatrix(self, size, elem):
        """
        :param size: The size of the matrix
        :return: A size*size matrix of zeroes
        """
        matrix = [elem for i in range(2)]
        matrix = [matrix for i in range(size)]
        matrix = [matrix for i in range(size)]
        return matrix

    def testPlaneFits(self):

        self.assertFalse(self.gc.planeFits(self.testMatrix, 0, 0))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 1, 1))

        self.assertTrue(self.gc.planeFits(self.testMatrix, 2, 2))
        self.assertTrue(self.gc.planeFits(self.testMatrix, 3, 3))
        self.assertTrue(self.gc.planeFits(self.testMatrix, 4, 4))
        self.assertTrue(self.gc.planeFits(self.testMatrix, 5, 5))

        self.assertFalse(self.gc.planeFits(self.testMatrix,6,7))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 7, 7))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 3, 6))
        self.assertFalse(self.gc.planeFits(self.testMatrix, 0, 5))

