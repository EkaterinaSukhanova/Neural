import numpy as np

from skimage.io import imread


def read_images(shape_name: str, predict_val: int) -> []:
    all_images = []
    for k in range(0, 3):
        file_name = "image_test/{}{}.png"
        new_filename = file_name.format(shape_name, k + 1)
        image_not_norm = imread(new_filename, as_grey=True)
        image = image_not_norm / 255
        image_and_predict = (np.reshape(image, image.shape[0] * image.shape[1]), predict_val)
        all_images.append(image_and_predict)

    return all_images


if __name__ == "__main__":
    read_images("circle", 1)
    read_images("triangle", 0)
