from copy import deepcopy


class Plane():
    def __init__(self, rotations, id):
        """
        A plane object stores the image of a plane and the number of rotations applied to it
        :param rotations: The number of rotations applied to the image, stored as %4 since 4 applied rotations is
                            identical to the original image
        :param id: the of the plane
        """
        self.__id = id # the id corresponding to all tiles belonging to the plane
        self.__image = self.__rotate(self.__getSource(), 5,
                                     rotations % 4)  # matrix of lists [tile_type, belongingPlane]
        self.__rotations = rotations % 4

    def getRotations(self):
        return self.__rotations

    def getImage(self):
        return self.__image

    def getId(self):
        return self.__id

    def __getSource(self):
        """
        :return: The image of a plane, stored as a 5x5 matrix containing pairs [value, belonging_plane]
        """
        image = [[[0, id], [0, id], [2, id], [0, id], [0, id]],
                 [[1, id], [1, id], [1, id], [1, id], [1, id]],
                 [[0, id], [0, id], [1, id], [0, id], [0, id]],
                 [[0, id], [1, id], [1, id], [1, id], [0, id]],
                 [[0, id], [0, id], [0, id], [0, id], [0, id]]]

        return image



    def __rotate(self, mat, size, times):
        """
        Rotate in place matrix mat of size size times times in the trig. direction
        :param mat: a n*n matrix to rotate
        :param size: the size of the matrix
        :param times: how many times to be rotated in trig. direction
        :return: None
        """
        matrix = deepcopy(mat)

        for k in range(times):
            for i in range(size//2):
                for j in range(i, size-i-1):
                    aux = matrix[i][j]
                    matrix[i][j] = matrix[j][size-i-1]
                    matrix[j][size-i-1] = matrix[size-i-1][size-j-1]
                    matrix[size-i-1][size-j-1] = matrix[size-j-1][i]
                    matrix[size-j-1][i] = aux

        return matrix

    def __buildMatrix(self, size, elem):
        """
        :param size: The size of the matrix
        :return: A size*size matrix of zeroes
        """
        matrix = [elem for i in range(2)]
        matrix = [matrix for i in range(size)]
        matrix = [matrix for i in range(size)]
        return matrix

    def destroy(self):
        """
        Mark the entire plane as hit
        :return: None
        """
        for i in range(5):
            for j in range(5):
                if self.__image[i][j][0] != 0:
                    self.__image[i][j][0] = 3

    def __str__(self):
        """
        :param n:
        :return:
        """
        output = ""
        for i in range(5):
            for j in range(5):
                output += str(self.__image[i][j][0])
            output += "\n"
        return output
