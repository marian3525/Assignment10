from random import randint


class Player():
    def __init__(self, targetingImage, namingScheme):
        """
        :param targetingImage: a 8*8 matrix which represents the discovered tiles and their type
        """
        self.__code = namingScheme
        self.__target = targetingImage

    def nextMove(self):
        """
        :return: [x,y] of the tile the gameController will have to fire at to hit the cockpit
        """
        for i in range(1, 6):
            for j in range(1, 6):
                # look for a suitable place to hit increasing the chances of a cockpit hit
                if i != -1 and j != -1:
                    if self.__target[i][j - 1][0] == self.__code["frame"] and self.__target[i][j + 1][0] == self.__code["frame"] and self.__target[i + 1][j][0] == self.__code["frame"] \
                            and self.__target[i][j][0] == self.__code["frame"]:
                        # (i,j) is a tile between the main wings of a plane rotated by 0 deg.
                        # the cockpit is at (i-1, j), attempt a hit
                        # 0 0 1 0 0
                        # 1 1 X 1 1
                        # 0 0 1 0 0
                        # 0 1 1 1 0
                        # 0 0 0 0 0
                        return [j, i - 1]

                    elif self.__target[i - 1][j][0] == self.__code["frame"] and self.__target[i + 1][j][0] == self.__code["frame"] and self.__target[i][j + 1][0] == self.__code["frame"] \
                            and self.__target[i][j][0] == self.__code["frame"]:
                        # plane rotated by 90 deg. to the left, cockpit at [i, j-1]
                        # 0 1 0 0 0
                        # 0 1 0 1 0
                        # 1 X 1 1 0
                        # 0 1 0 1 0
                        # 0 1 0 0 0
                        return [j - 1, i]

                    elif self.__target[i][j - 1][0] == self.__code["frame"] and self.__target[i][j + 1][0] ==self.__code["frame"] and self.__target[i - 1][j][0] == self.__code["frame"] \
                            and self.__target[i][j][0] == self.__code["frame"]:
                        # 180 deg left
                        # 0 0 0 0 0
                        # 0 1 1 1 0
                        # 0 0 1 0 0
                        # 1 1 X 1 1
                        # 0 0 1 0 0
                        return [j, i + 1]

                    elif self.__target[i][j - 1][0] == self.__code["frame"] and self.__target[i - 1][j][0] == self.__code["frame"] and self.__target[i + 1][j][0] == self.__code["frame"] \
                            and self.__target[i][j][0] == self.__code["frame"]:
                        # 270 deg. left
                        # 0 0 0 1 0
                        # 0 1 0 1 0
                        # 0 1 1 X 1
                        # 0 1 0 1 0
                        # 0 0 0 1 0
                        return [j + 1, i]

        # not a standard case, pick and attack a random tile around the n-th tile found, which is !=-1
        n = randint(49)
        k = 0
        for i in range(1, 7):
            for j in range(1, 7):
                if self.__target[i][j] is not -1:
                    k += 1
                if k == n:
                    offset1 = randint(-1, 1)
                    offset2 = randint(-1, 1)
                    i += offset1
                    j += offset2
                    return [j,i]
