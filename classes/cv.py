import base64
from pathlib import Path

import cv2 as cv
import numpy as np


class CvImage:
    """
    Wrapper for OpenCV image object
    :param image: Path to image file or base64 string
    :param flags: OpenCV flags for cv.imread function. Default is cv.IMREAD_GRAYSCALE
    :var cv_image: OpenCV image object
    """
    def __init__(self, image: Path or str, flags=cv.IMREAD_GRAYSCALE):
        if isinstance(image, str):
            image_64_decode = base64.b64decode(image)
            image_array = np.frombuffer(image_64_decode, dtype=np.uint8)
            self.cv_image = cv.imdecode(image_array, flags=flags)
        elif isinstance(image, Path):
            self.cv_image = cv.imread(str(image), flags)
        else:
            raise TypeError("Unknown type! Input should be base64 string or Path object with path to image file")


def find_templ_in_img(image: CvImage, templ: CvImage):
    """
    Find template in image using OpenCV matchTemplate function
    :param image: CvImage object
    :param templ: CvImage object
    :return: tuple (max_loc, max_val)
    max_loc - (x, y) coordinates of the top left corner of the template in the image
    max_val - value of the match
    """
    if image.cv_image.ndim == 2:
        image.cv_image = cv.cvtColor(image.cv_image, cv.COLOR_GRAY2BGR)
    if templ.cv_image.ndim == 2:
        templ.cv_image = cv.cvtColor(templ.cv_image, cv.COLOR_GRAY2BGR)
    result = cv.matchTemplate(image.cv_image, templ.cv_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    return max_loc, max_val
