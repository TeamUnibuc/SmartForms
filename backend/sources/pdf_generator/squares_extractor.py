from shutil import Error
from typing import Any, List, Tuple
import fpdf
import qrcode
import random
import os
import cv2 as cv
import pdf2image
import matplotlib.pyplot as plt
import numpy as np
import math
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




class FormImageTransformer:
    """Class reading data from a given form
    and performing a 4-points perspective change.
    """
    _image: np.ndarray
    image_after_perspective_change: np.ndarray
    qr_content: str
    top_left_corner: Tuple[int, int]
    top_right_corner: Tuple[int, int]
    bottom_left_corner: Tuple[int, int]
    bottom_right_corner: Tuple[int, int]
    _qr_code_area: float
    
    def _open_qr_code(self):
        """Searches for a QR code in the image,
        and saves its top-right corner, its area and
        its content
        """
        qrCodeDetector = cv2.QRCodeDetector()
        decodedText, points, _ = qrCodeDetector.detectAndDecode(self._image)
        if len(points) != 1:
            raise Exception("Invalid number of QR codes found!")
        int_points: np.ndarray = points.astype(int)

        self.top_right_corner = (int_points[0][1][0], int_points[0][1][1])
        self.qr_code_area = cv2.contourArea(int_points)
        self.qr_content = decodedText

    def _is_marker(self, poly: np.ndarray) -> Tuple[bool, Tuple[int, int]]:
        """Checks if a polygon is or not a marker
        
        Arguments:
            poly -- List of vertices of the polygon

        Returns:
            true / false -- if the polygon is or not a marker
            (X, Y) -- position of the outside vertice if it's a marker
        """
        
        # markers should have 6 vertices
        if len(poly) != 6:
            return (False, (-1, -1))

        poly = poly.astype(int)
        area = cv2.contourArea(poly)
        
        distances = []
        for i in range(6):
            d = np.linalg.norm(poly[i] - poly[i - 1])
            # print(d)
            distances.append(d)

        distances.sort()

        # pairs of edges must be equal
        for i in [0, 2, 4]:
            if distances[i + 1] > distances[i] * MARKER_MATCHING_TOLERANCE:
                return (False, (-1, -1))

        # TODO: Check relative size between edges
        # TODO: Check size compared to QR code
        area_rap = area / self.qr_code_area
        if area_rap < 0.05:
            return (False, (-1, -1))

        # check area matches

        # AREA_TOLERANCE = 1.5
        computed_area = distances[-1]**2 - distances[2]**2
        if area > computed_area * MARKER_MATCHING_TOLERANCE or area * MARKER_MATCHING_TOLERANCE < computed_area:
            return (False, (-1, -1))

        # search extern edge
        for i in [-1, 0, 1, 2, 3, 4]:
            d_prev = np.linalg.norm(poly[i] - poly[i - 1])
            d_next = np.linalg.norm(poly[i + 1] - poly[i])

            if d_prev >= distances[4] and d_next >= distances[4]:
                return (True, (poly[i][0][0], poly[i][0][1]))
        
        return (False, (-1, -1))

    def _find_markers(self):
        #convert from BGR to HSV color space
        gray: np.ndarray = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        gray = gray + 255 / 2 - gray.mean()
        gray[gray > 255] = 255
        gray[gray < 0] = 0
        gray = gray.astype(np.uint8)

        #apply threshold
        threshold = cv2.threshold(gray, IMAGE_BLACK_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
        
        contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        result = self._image.copy()

        points: List[Tuple[int, int]] = []

        for c in contours:
            # TODO: Check if this is ok
            # https://docs.opencv.org/3.4.14/dd/d49/tutorial_py_contour_features.html
            epsilon = POLYGON_APROXIMATION_EPSILON * cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            # cv2.drawContours(result, [approx], -1, (0, 255, 0), 1)

            is_marker, (X, Y) = self._is_marker(approx.copy())

            if is_marker:
                print("Found new marker!")
                cv2.drawContours(result, [approx], -1, (0, 255, 0), 1)
                points.append((X, Y))

        plt.imshow(threshold)
        plt.show()

        def is_trig(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> bool:
            d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            return d <= 0
        
        if len(points) != 3:
            raise Error("Not found markers! Found " + str(points) + " markers instead of 3!!")

        if not is_trig(self.top_right_corner, points[0], points[1]):
            points[0], points[1] = points[1], points[0]
        if not is_trig(self.top_right_corner, points[0], points[2]):
            points[0], points[2] = points[2], points[0]
        if not is_trig(self.top_right_corner, points[1], points[2]):
            points[1], points[2] = points[2], points[1]

        self.top_left_corner = points[0]
        self.bottom_left_corner = points[1]
        self.bottom_right_corner = points[2]

        cv2.circle(result, self.top_right_corner, radius=10, color=(0, 0, 255), thickness=10)
        cv2.circle(result, self.top_left_corner, radius=10, color=(0, 0, 255), thickness=10)
        cv2.circle(result, self.bottom_left_corner, radius=10, color=(255, 0, 0), thickness=10)
        cv2.circle(result, self.bottom_right_corner, radius=10, color=(0, 255, 0), thickness=10)
        
        plt.imsave("Image.jpg", result)

    def _compute_perspective_transform(self):
        """Creates the `image_after_perspective_change` object,
        such that the 4 corners are in a rectangle.
        """
        # https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
        tl = self.top_left_corner
        tr = self.top_right_corner
        br = self.bottom_right_corner
        bl = self.bottom_left_corner

        rect = (tl, tr, br, bl)
        rect = [[rect[i][j] for j in [0, 1]] for i in range(4)]
        rect = np.array(rect)
        rect = rect.astype(np.float32)
        print(rect.shape)

        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(self._image, M, (maxWidth, maxHeight))
        # return the warped image
        self.image_after_perspective_change = warped

    def __init__(self, image):
        self._image = image

        self._open_qr_code()
        self._find_markers()
        self._compute_perspective_transform()
