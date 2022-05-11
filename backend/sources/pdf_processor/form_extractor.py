import logging
import os
from typing import Dict, List, Tuple, Union
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
from pyzbar.pyzbar import decode


DEBUG = False

def change_image_perspective(picture: np.ndarray, template: np.ndarray) -> np.ndarray:
    """
        Changes the perspective of the picture, to make it look like the template
    """
    # TODO:
    # https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
    # NOT apply a threshold on the final image
    # i.e. return a copy of the image WITHOUT a threshold
    # as it reduces the quality of the image

    def preprocess(img):
        if len(img.shape) == 3 and img.shape[2] == 3:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, img = cv.threshold(img, 180, 255, cv.THRESH_BINARY)
        return img
        
    picture_not_processed = picture.copy()
    picture = preprocess(picture)
    template = preprocess(template)

    orb = cv.ORB_create(nfeatures=10000)
    kp1, des1 = orb.detectAndCompute(picture, None)
    kp2, des2 = orb.detectAndCompute(template, None)

    index_params = dict(algorithm=6,
                        table_number=12,
                        key_size=20,
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

    if DEBUG:
        print("Corected picture + template:")
        plt.imshow((corrected_img + template) // 2)
        plt.show()

    return corrected_img

def extract_form_id_content_from_image(picture: np.ndarray) -> str:
    """
    Extracts the QR code content from an image.
    Returns: the QR code, if readable, '' if nothing is found.
    """
    # We use the pyzbar module, as opencv doesn't work for big images.
    # this requires special packages:
    # https://pypi.org/project/pyzbar/
    # for fedora, use `zbar`

    qr_codes = decode(picture)

    # no qr code was found
    if len(qr_codes) == 0:
        return ''
    
    # extract qr code
    content = str(qr_codes[0].data, encoding='utf-8')

    # should start with the URL prefix
    assert content.startswith(os.environ["FORM_ID_PREFIX"])

    # remove the prefix from the ID
    return content[len(os.environ["FORM_ID_PREFIX"]):]

def extract_question_answer_from_form(
        fixed_pages: Dict[int, np.ndarray],
        question: Union[smart_forms_types.FormTextQuestion, smart_forms_types.FormMultipleChoiceQuestion],
        squares_location: List[smart_forms_types.Square]) -> List[str]:
    """
        fixed_picture: mapping for each page of the form where we already fixed the perspective transform.
        question: question we are trying to extract.
        square_locations: location of the squares of the question we are interested in.
        Returns the result
    """

    # the content, and the nr of the square in the question
    # i.e., the first square of the question will be nr 0, next nr 1 etc.
    # this is used because if a page is missing, then the square is also missing.
    squares_content, squares_nr = [], []

    for square_nr, square in enumerate(squares_location):

        if square.page not in fixed_pages:
            logging.debug(f"Unable to find question #{question.title}, as page {square.page} is missing.")
            continue

        # page the square is in
        fixed_page = fixed_pages[square.page]
        
        # rescaling factor
        multiplier_h = fixed_page.shape[0] / constants.PDF_H
        multiplier_w = fixed_page.shape[1] / constants.PDF_W

        # actual square position
        x = int(multiplier_h * square.x)
        y = int(multiplier_w * square.y)
        dx = int(multiplier_h * square.width)
        dy = int(multiplier_w * square.width)

        # draw square, for debug
        # TODO: maybe delete this?
        cv.rectangle(fixed_page, (x, y), (x+dx, y+dy), (0, 255, 255), thickness=2)

        # This offset makes sure we don't include any borders in the square character.
        # TODO: if we switch to our own dataset, then maybe excluding the border won't
        # be required.
        SQUARES_OFFSET = 10
        sq_img = fixed_page[
            y + SQUARES_OFFSET : y + dy - SQUARES_OFFSET,
            x + SQUARES_OFFSET : x + dx - SQUARES_OFFSET
        ]
        squares_content.append(sq_img)
        squares_nr.append(square_nr)


    # if DEBUG:
    #     plt.imshow(fixed_picture)
    #     plt.show()

    # convert square array to a ndarray, and perform OCR
    squares_content = np.stack(squares_content)

    # find allowed characters, depending on the type of question
    # TODO:
    allowed_characters = (
        question.allowedCharacters
        if isinstance(question, smart_forms_types.FormTextQuestion)
        else " X*+"
    )
    squares_predictions = ocr.predict_characters(squares_content, allowed_characters)

    # compute the initial answer
    answer = ["?" for i in range(len(squares_location))]

    for square_nr, square_prediction in zip(squares_nr, squares_predictions):
        answer[square_nr] = square_prediction

    return "".join(answer)



def extract_answer_from_form(
            pdf_form: smart_forms_types.PdfForm,
            page_to_img: Dict[int, np.ndarray]) -> smart_forms_types.FormAnswer:
    """
    Extracts as much as possible from the content of a single form, whose pages
    are saved in page_to_img (note that not all pages must be present).
    """
    # convert to grayscale
    # TODO: Check if bgr or rbg
    page_to_img_gray = {
        i: cv.cvtColor(page_to_img[i], cv.COLOR_BGR2GRAY) for i in page_to_img
    }
    
    template_imgs = pdf2image.convert_from_bytes(pdf_form.extract_raw_pdf_bytes())
    template_imgs = [np.array(i) for i in template_imgs]

    page_to_img_fixed = {
        i: change_image_perspective(
            page_to_img_gray[i],
            template_imgs[i]
        ) for i in page_to_img_gray
    }

    answers = []

    for question, squares in zip(pdf_form.description.questions, pdf_form.answer_squares_location):
        answers.append(extract_question_answer_from_form(page_to_img_fixed, question, squares))


    form_answer = smart_forms_types.FormAnswer(
        answerId="",
        formId=pdf_form.description.formId,
        userId="",
        answers=answers,
        authorEmail=""
    )

    return form_answer
