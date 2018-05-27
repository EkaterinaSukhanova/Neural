import numpy as np

from skimage.io import imread


def read_one_image(name: str) -> []:

    read_image = imread(name, as_grey=True)
    image_norm = read_image / 255,
    one_image = (np.reshape(image_norm, image_norm.shape[0] * image_norm.shape[1]))

    return one_image


if __name__ == "__main__":
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            print(image[i][j], end=" ")
        print("")
