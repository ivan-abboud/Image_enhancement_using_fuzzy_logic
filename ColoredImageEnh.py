import numpy as np
from scipy.interpolate import interp1d
from utils import utils

epsilon = 0.000001
utils = utils()

class ColoredImageEnh:
    def __init__(self, image, n, m, gamma):
        """
        Initializing the model and it's variables
        :param image: image to be enhanced
        :param n: number of windows in width
        :param m: number of windows in height
        :param gamma: fuzzification coffecient
        """
        self.image = image
        self.n = n
        self.m = m
        self.gamma = gamma

        # Membership matrix of pixels to each window
        self.pixelMemberships = np.full((n, m, image.shape[0], image.shape[1]), -1000, dtype=np.float)
        # Mean of each window
        self.windowsMean = np.full((n, m), -1000, dtype=np.float)
        # Cardinality of each window
        self.windowsCard = np.full((n, m), -1000, dtype=np.float)
        self.pijMat = np.full((n, m, image.shape[0], image.shape[1]), -1000, dtype=np.float)
        # Variance of each window
        self.windowsVariance = np.full((n, m), -1000, dtype=np.float)

        self.image = self.convertImgDown(self.image)
        self.epsilon = 0.00001
        # Luminosity matrix of colored image
        self.lum = np.full((image.shape[0] , image.shape[1]) , -1000 , dtype=np.float)

    def convertImgDown(self, image):
        """
        Mapping pixel values from interval [0 , 255] to [-1 , 1]
        :param image: image needed to be converted
        :return: image after mapping it to interval [-1 , 1]
        """
        mapping = interp1d([0, 255], [-1, 1])
        image = mapping(image)
        return image

    def convertImgUp(self, img):
        """
        Mapping pixel values from interval [-1 , 1] to interval [0 , 255]
        :param img: image needed to be converted
        :return: image after mapping
        """
        mapping = interp1d([np.min(img), np.max(img)], [0, 255])
        img = mapping(img)
        return img

    def imageLuminosity(self,i,j):
        """
        Calculating the Luminosity of colored image at index i , j
        :param i: row index
        :param j: column index
        :return: The luminosity value at index [i j]
        """
        if self.lum[i][j] == -1000:
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    temp = utils.add(self.image[x][y][2] , self.image[x][y][1])
                    temp = utils.add(temp , self.image[x][y][0])
                    self.lum[x][y] = utils.mult(1/3 , temp)
        return self.lum[i][j]


    def qxi(self, i, x):
        """
        Calculating formula:
        :param i:
        :param x:
        :return:
        """
        x0 = 0
        x1 = self.image.shape[0]
        nCi = utils.comb(self.n, i)
        nom = ((x - x0) ** i) * ((x1 - x) ** (self.n - i))
        denom = (x1 - x0) ** self.n
        ans = nCi * nom / denom
        return ans

    def qyj(self, j, y):
        y0 = 0
        y1 = self.image.shape[1]
        nCi = utils.comb(self.m, j)
        nom = (np.power((y - y0), j)) * (np.power((y1 - y), (self.m - j)))
        denom = (y1 - y0) ** self.m
        ans = nCi * nom / denom
        return ans

    def pij(self, i, j, x, y):
        if self.pijMat[i][j][x][y] == -1000:
            ans = self.qxi(i, x) * self.qyj(j, y)
            self.pijMat[i][j][x][y] = ans
        return self.pijMat[i][j][x][y]

    def membership(self, i, j, x, y):
        """
        Calculating the membership of pixel [x][y] to a window i,j
        :param i: window row index
        :param j: window column index
        :param x: pixel row index
        :param y: pixel column index
        :return: Membership value
        """
        if self.pixelMemberships[i][j][x][y] == -1000:
            nom = self.pij(i, j, x, y) ** self.gamma
            denom = 0
            for idx1 in range(self.n):
                for idx2 in range(self.m):
                    denom += np.power(self.pij(idx1, idx2, x, y), self.gamma)
            ans = nom / (denom + epsilon)
            self.pixelMemberships[i][j][x][y] = ans
        return self.pixelMemberships[i][j][x][y]

    def windowCard(self, i, j):
        """
        Calculating the cardinality of window i,j
        :param i:
        :param j:
        :return: window card value
        """
        if self.windowsCard[i][j] == -1000:
            card = 0.0
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    card += self.membership(i, j, x, y)
            self.windowsCard[i][j] = card
        return self.windowsCard[i][j]

    def windowMean(self, i, j):
        """
        Calculating the mean of window i,j
        :param i:
        :param j:
        :return: Mean value
        """
        if self.windowsMean[i][j] == -1000:
            card = self.windowCard(i, j)
            mean = 0.0
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    mean = utils.add(mean, utils.mult(self.membership(i, j, x, y) / card, self.imageLuminosity(x,y)))
            self.windowsMean[i][j] = mean
        return self.windowsMean[i][j]

    def windowVar(self, i, j):
        """
        Calculating the squared Variance of a window
        :param i:
        :param j:
        :return: Squared variance value
        """
        if self.windowsVariance[i][j] == -1000:
            var = 0.0
            card = self.windowCard(i, j)
            mean = self.windowMean(i, j)
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    memship = self.membership(i, j, x, y)
                    nom = memship * (utils.norm(utils.subtract(self.imageLuminosity(x,y), mean)) ** 2)
                    denom = card
                    var += nom / denom
            self.windowsVariance[i][j] = var
        return self.windowsVariance[i][j]

    def imageEnhance(self):
        """
        Iterating over the channels , pixel and windows and calculate the new image after enhancing
        :return: Enhanced image after converting it to interval[0,255]
        """
        final_img = np.zeros((self.image.shape[0] , self.image.shape[1] , 3) , dtype=np.float)
        sigma = np.sqrt(1/3)
        for chn in range(3):
            for i in range(self.n):
                for j in range(self.m):
                    var = np.sqrt(self.windowVar(i,j))
                    mean = self.windowMean(i,j)
                    for x in range(self.image.shape[0]):
                        for y in range(self.image.shape[1]):
                            memship = self.membership(i, j, x, y)
                            final_img[x][y][chn] += utils.mult((memship*sigma/var) , utils.subtract(self.image[x][y][chn] , mean))

        final_img = self.convertImgUp(final_img)

        return final_img






