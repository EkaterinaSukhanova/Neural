import numpy as np

from skimage.io import imread


image = imread("image_test/circle1.png", as_grey=True)
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        print(image[i][j], end=" ")
    print("")
