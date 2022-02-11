from shutil import Error
from typing import Any, List, Tuple
import cv2 as cv
import pdf2image
import matplotlib.pyplot as plt
import numpy as np
import database, smart_forms_types
from .constants import *

def change_image_perspective(picture: np.ndarray, template: np.ndarray) -> np.ndarray:
    """
        Changes the perspective of the picture, to make it look like the template
    """
    def preprocess(img):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, img = cv.threshold(img, 128, 255, cv.THRESH_BINARY)
        return img 
    picture = preprocess(picture)
    template = preprocess(template)

    orb = cv.ORB_create(nfeatures=10000)
    kp1, des1 = orb.detectAndCompute(picture, None)
    kp2, des2 = orb.detectAndCompute(template, None)

    index_params = dict(algorithm=6,
                        table_number=6,
                        key_size=12,
                        multi_probe_level=2)
    search_params = {}
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # As per Lowe's ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    src_points = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_points = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    m, mask = cv.findHomography(src_points, dst_points, cv.RANSAC, 5.0)
    corrected_img = cv.warpPerspective(picture, m, (template.shape[1], template.shape[0]))

    return corrected_img

def find_maching_template(picture: np.ndarray) -> smart_forms_types.PdfForm:
    """
        Searches for the QR code and finds the ID.
    """
    qrCodeDetector = cv.QRCodeDetector()
    formId, points, _ = qrCodeDetector.detectAndDecode(picture)
    if len(points) != 1:
        raise Exception("Invalid number of QR codes found!")

    form_dict = [i for i in database.get_collection(database.FORMS).find({ "formId": formId })]
    form = smart_forms_types.pdf_form_from_dict(form_dict[0])
    return form
