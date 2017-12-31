import unittest
from Domain.Plane import Plane


class TestDomain(unittest.TestCase):

    def setUp(self):
        self.plane = Plane(0, 0)

    def testRotatePlane(self):
        plane = Plane(0, 0)
        # 00200
        # 11111
        # 00100
        # 01110
        # 00000
        self.assertEqual(plane.getImage()[0][0][0], 0)
        self.assertEqual(plane.getImage()[0][2][0], 2)
        self.assertEqual(plane.getImage()[2][2][0], 1)
        self.assertEqual(plane.getImage()[2][1][0], 0)

        # 1 rotation
        plane = Plane(1, 0)
        # 01000
        # 01010
        # 21110
        # 01010
        # 01000
        self.assertEqual(plane.getImage()[0][0][0], 0)
        self.assertEqual(plane.getImage()[0][1][0], 1)
        self.assertEqual(plane.getImage()[2][0][0], 2)
        self.assertEqual(plane.getImage()[4][1][0], 1)

    def testBuildPlanes(self):
        plane = Plane(0, 0)

        self.assertEqual(plane.getImage()[0][0][0], 0)
        self.assertEqual(plane.getImage()[0][2][0], 2)
        self.assertEqual(plane.getImage()[2][2][0], 1)
        self.assertEqual(plane.getImage()[2][1][0], 0)

        self.assertEqual(plane.getRotations(), 0)
        self.assertEqual(str(plane), "00200\n11111\n00100\n01110\n00000\n")

    def testDestroy(self):

        self.assertEqual(self.plane.getImage()[0][0][0], 0)
        self.assertEqual(self.plane.getImage()[0][2][0], 2)
        self.assertEqual(self.plane.getImage()[2][2][0], 1)
        self.assertEqual(self.plane.getImage()[2][1][0], 0)

        self.plane.destroy()

        self.assertEqual(self.plane.getImage()[0][0][0], 0)
        self.assertEqual(self.plane.getImage()[0][2][0], 3)
        self.assertEqual(self.plane.getImage()[2][2][0], 3)
        self.assertEqual(self.plane.getImage()[2][1][0], 0)
