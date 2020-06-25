import cv2
import ImageEnh
import numpy as np
import ColoredImageEnh


n=2
m=2
gamma=4
img_name = 'island'

def colored_enhancing():
    img = cv2.imread(img_name + '.png')
    print(img.shape)
    imgEnh = ColoredImageEnh.ColoredImageEnh(img, n, m, gamma)
    final_image = imgEnh.imageEnhance()
    final_image = np.array(final_image, dtype=np.uint8)
    cv2.imshow('before converting', img)
    cv2.imshow('final', final_image)
    cv2.imwrite(img_name + str(n) + 'x' + str(m) + 'x' + str(gamma) + '.png', final_image)
    print(final_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def gray_enhancing():
    img = cv2.imread(img_name + '.png')
    print(img.shape)
    img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    imgEnh = ImageEnh.ImageEnh(img ,n,m,gamma)
    final_image = imgEnh.enhanceImage()
    final_image = np.array(final_image , dtype = np.uint8)
    cv2.imshow('before converting' , img)
    cv2.imshow('final' , final_image)
    cv2.imwrite(img_name+str(n)+'x'+str(m)+'x'+str(gamma)+'.png' , final_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

colored_enhancing()