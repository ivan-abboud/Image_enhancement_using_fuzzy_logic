import numpy as np
from scipy.interpolate import interp1d
import math
from utils import utils

epsilon = 0.00001
utils = utils()
class ImageEnh:
    def __init__(self, image, n, m, gamma):
        self.image = image
        self.n = n
        self.m = m
        self.gamma = gamma
        self.pixelMemberships = np.full((n, m, image.shape[0], image.shape[1]), -1000 , dtype=np.float)
        self.windowsMean = np.full((n, m), -1000 ,dtype=np.float)
        self.windowsCard = np.full((n, m), -1000 , dtype=np.float)
        self.pijMat = np.full((n, m, image.shape[0], image.shape[1]), -1000,dtype=np.float)
        self.windowsVariance = np.full((n, m), -1000,dtype=np.float)
        self.image = self.convertImgDown(self.image)
        self.epsilon = 0.00001


    def convertImgDown(self, image):
        mapping = interp1d([0, 255], [-1, 1])
        image = mapping(image)
        #         for x in range(self.image.shape[0]):
        #             for y in range(self.image.shape[1]):
        #                 self.image[x][y] = (((self.image[x][y]) * (2)) / (255)) - 1
        return image

    def convertImgUp(self, img):
        num1 = np.abs(np.min(img))
        num2 = np.abs(np.max(img))
        mapping = interp1d([-1*max(num1,num2), max(num1,num2)], [0, 255])
        img = mapping(img)
        #         new_img = np.zeros((self.image.shape[0] , self.image.shape[1]))
        #         for x in range(self.image.shape[0]):
        #             for y in range(self.image.shape[1]):
        #                 new_img[x][y] = (((img[x][y] + 1) * (255)) / (2))
        return img

    def qxi(self, i, x):
        x0 = 0
        x1 = self.image.shape[0]
        nCi = utils.comb(self.n, i)
        nom = ((x - x0) ** i) * ((x1 - x) ** (self.n - i))
        denom = (x1 - x0) ** self.n
        ans = nCi * nom / denom
        # if ans > 1 or ans < 0:
        #     print('Error in qxi : ', ans)
        return ans

    def qyj(self, j, y):
        y0 = 0
        y1 = self.image.shape[1]
        nCi = utils.comb(self.m, j)
        nom = (np.power((y - y0),j)) * (np.power((y1 - y) , (self.m - j)))
        denom = (y1 - y0) ** self.m
        ans = nCi * nom / denom
        # if ans > 1 or ans < 0:
        #     print('Error in qyj : ', ans)
        return ans

    def pij(self, i, j, x, y):
        if self.pijMat[i][j][x][y] == -1000:
            ans = self.qxi(i, x) * self.qyj(j, y)
            # if ans > 1 or ans < 0:
            #     print('Error in pij : ', i, j, ans)
            self.pijMat[i][j][x][y] = ans
        return self.pijMat[i][j][x][y]

    def membership(self, i, j, x, y):
        if self.pixelMemberships[i][j][x][y] == -1000:
            nom = self.pij(i, j, x, y) ** self.gamma
            denom = 0
            for idx1 in range(self.n):
                for idx2 in range(self.m):
                    denom += np.power(self.pij(idx1, idx2, x, y), self.gamma)
            ans = nom / (denom + epsilon)
            if ans > 1 or ans < 0 or math.isnan(ans):
                print('Error in membership : ', denom)
            self.pixelMemberships[i][j][x][y] = ans
        return self.pixelMemberships[i][j][x][y]

    def windowCard(self, i, j):
        if self.windowsCard[i][j] == -1000:
            card = 0.0
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    card += self.membership(i, j, x, y)
            self.windowsCard[i][j] = card
        return self.windowsCard[i][j]

    def windowMean(self, i, j):
        if self.windowsMean[i][j] == -1000:
            card = self.windowCard(i, j)
            mean = 0.0
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    mean = utils.add(mean, utils.mult(self.membership(i, j, x, y) / card, self.image[x][y]))
            self.windowsMean[i][j] = mean
        return self.windowsMean[i][j]

    def windowVar(self, i, j):
        if self.windowsVariance[i][j] == -1000:
            var = 0.0
            card = self.windowCard(i, j)
            mean = self.windowMean(i, j)
            for x in range(self.image.shape[0]):
                for y in range(self.image.shape[1]):
                    memship = self.membership(i, j, x, y)
                    nom = memship * (utils.norm(utils.subtract(self.image[x][y], mean)) ** 2)
                    denom = card
                    var += nom / denom
            self.windowsVariance[i][j] = var
        return self.windowsVariance[i][j]

    def enhanceImage(self):
        image_copy = np.zeros((self.image.shape[0], self.image.shape[1]))
        sigma = np.sqrt(1/3)
        for i in range(self.n):
            for j in range(self.m):
                mean = self.windowMean(i, j)
                variance = np.sqrt(self.windowVar(i, j))
                for x in range(self.image.shape[0]):
                    for y in range(self.image.shape[1]):
                        left = sigma / variance
                        psi = utils.mult(left, utils.subtract(self.image[x][y], mean))
                        memship = self.membership(i, j, x, y)
                        image_copy[x][y] += utils.mult(memship, psi)
        image_copy = self.convertImgUp(image_copy)
        return image_copy