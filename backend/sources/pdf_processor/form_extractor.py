import logging
from typing import List, Tuple
import cv2 as cv
import pdf2image
import matplotlib.pyplot as plt
import numpy as np
import database, smart_forms_types
from .constants import *
import pdf_processor.constants as constants
import ocr
import io
from PIL import Image

DEBUG = False

def change_image_perspective(picture: np.ndarray, template: np.ndarray) -> np.ndarray:
    """
        Changes the perspective of the picture, to make it look like the template
    """
    # TODO:
    # NOT apply a threshold on the final image
    # i.e. return a copy of the image WITHOUT a threshold
    # as it reduces the quality of the image
    
    def preprocess(img):
        if len(img.shape) == 3 and img.shape[2] == 3:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, img = cv.threshold(img, 100, 255, cv.THRESH_BINARY)
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
        We first search in the entire image.
    """
    def get_form_id_from_image(picture: np.ndarray) -> str:
        qrCodeDetector = cv.QRCodeDetector()
        form_id, points, _ = qrCodeDetector.detectAndDecode(picture)
        
        if points is None or len(points) != 1:
            # didn't find form_id
            return ''
        return form_id

    form_id = get_form_id_from_image(picture)

    while form_id == '' and picture.shape[0] > 500:
        # we try to extract the QR code.
        # if the image has a resolution too high, then we won't be able
        # to find it, so we scale it down.

        picture = cv.resize(picture, dsize=(0, 0), fx=0.8, fy=0.8)
        form_id = get_form_id_from_image(picture)


    form_dict = [i for i in database.get_collection(database.FORMS).find({ "formId": form_id })]

    # unable to find form
    if len(form_dict) == 0:
        raise Exception(f"Unable to find form {form_id} on mongo cloud!")

    form = smart_forms_types.pdf_form_from_dict(form_dict[0])
    return form

def extract_content_from_form(fixed_picture: np.ndarray, form: smart_forms_types.PdfForm) -> List[List[str]]:
    """
        fixed_picture: image where we already fixed the perspective transform.
        Returns a list of squares.
    """

    squares_content = []
    multiplier_h = fixed_picture.shape[0] / constants.PDF_H
    multiplier_w = fixed_picture.shape[1] / constants.PDF_W
            
    for squares in form.answer_squares_location:
        question_content = []
        for square in squares:
            x = int(multiplier_h * square.x)
            y = int(multiplier_w * square.y)
            dx = int(multiplier_h * square.width)
            dy = int(multiplier_w * square.width)
            
            cv.rectangle(fixed_picture, (x, y), (x+dx, y+dy), (0, 255, 255), thickness=2)

            # This offset makes sure we don't include any borders in the square character.
            # TODO: if we switch to our own dataset, then maybe excluding the border won't
            # be required.
            SQUARES_OFFSET = 10
            sq_img = fixed_picture[
                y + SQUARES_OFFSET : y + dy - SQUARES_OFFSET,
                x + SQUARES_OFFSET : x + dx - SQUARES_OFFSET
            ]
            question_content.append(sq_img)
        
        if DEBUG:
            plt.imshow(fixed_picture)
            plt.show()

        squares_content.append(ocr.predict_characters(np.stack(question_content)))


    return squares_content

def pdf_to_numpy(file: bytes) -> np.array:
    """
        converts a pdf binary to a numpy array
    """
    image = pdf2image.convert_from_bytes(file)[0]
    image = np.array(image)
    return image

def extract_answer_from_form(file: bytes, filename: str) -> Tuple[smart_forms_types.PdfForm, smart_forms_types.FormAnswer]:
    """
        Processes a file, extracting the content of its answer squares.
        The file has to be an image or a pdf.
    
        TODO: Support zip files.
    """
    if filename[-4:] == ".pdf": # pdf file
        image = pdf_to_numpy(file)
        # TODO: Handle multiple pages
    else: # try to read as image
        image = np.array(Image.open(io.BytesIO(file)))

    logging.debug(f"Image shape: {image.shape}")

    # convert to grayscale
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # find form.
    form = find_maching_template(image)
    fixed_image = change_image_perspective(image, pdf_to_numpy(form.extract_raw_pdf_bytes()))

    if DEBUG:
        print("Fixed image:", flush=True)
        plt.imshow(fixed_image)
        plt.show()

    content = extract_content_from_form(fixed_image, form)
    content = ["".join(i) for i in content]

    form_answer = smart_forms_types.FormAnswer(
        answerId="",
        formId=form.description.formId,
        userId="",
        answers=content
    )

    return (form, form_answer)
