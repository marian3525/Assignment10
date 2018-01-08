import unittest
from Domain.Plane import Plane


class TestDomain(unittest.TestCase):

    def setUp(self):
        self.__tileCode = {"air": 1, "frame": 2, "hit": 3, "cockpit": 4, "unknown": 0}
        self.plane = Plane(0, 0, self.__tileCode)

    def testRotatePlane(self):
        plane = Plane(0, 0)
        # 00200
        # 11111
        # 00100
        # 01110
        # 00000
        self.assertEqual(plane.getImage()[0][0][0], self.__tileCode["air"])
        self.assertEqual(plane.getImage()[0][2][0], self.__tileCode["cockpit"])
        self.assertEqual(plane.getImage()[2][2][0], self.__tileCode["frame"])
        self.assertEqual(plane.getImage()[2][1][0], self.__tileCode["air"])

        # 1 rotation
        plane = Plane(1, 0, self.__tileCode)
        # 01000
        # 01010
        # 21110
        # 01010
        # 01000
        self.assertEqual(plane.getImage()[0][0][0], self.__tileCode["air"])
        self.assertEqual(plane.getImage()[0][1][0], self.__tileCode["frame"])
        self.assertEqual(plane.getImage()[2][0][0], self.__tileCode["cockpit"])
        self.assertEqual(plane.getImage()[4][1][0], self.__tileCOde["air"])

    def testBuildPlanes(self):
        plane = Plane(0, 0)

        self.assertEqual(plane.getImage()[0][0][0], self.__tileCode["air"])
        self.assertEqual(plane.getImage()[0][2][0], self.__tileCode["cockpit"])
        self.assertEqual(plane.getImage()[2][2][0], self.__tileCode["frame"])
        self.assertEqual(plane.getImage()[2][1][0], self.__tileCode["air"])

        self.assertEqual(plane.getRotations(), 0)
        # self.assertEqual(str(plane), "00200\n11111\n00100\n01110\n00000\n")

    def testDestroy(self):

        self.assertEqual(self.plane.getImage()[0][0][0], self.__tileCode["air"])
        self.assertEqual(self.plane.getImage()[0][2][0], self.__tileCode["cockpit"])
        self.assertEqual(self.plane.getImage()[2][2][0], self.__tileCode["frame"])
        self.assertEqual(self.plane.getImage()[2][1][0], self.__tileCode["air"])

        self.plane.destroy()

        self.assertEqual(self.plane.getImage()[0][0][0], self.__tileCode["air"])
        self.assertEqual(self.plane.getImage()[0][2][0], self.__tileCode["hit"])
        self.assertEqual(self.plane.getImage()[2][2][0], self.__tileCode["hit"])
        self.assertEqual(self.plane.getImage()[2][1][0], self.__tileCode["air"])
