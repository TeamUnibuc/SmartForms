import logging
import os
import pickle
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
    # https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
    def preprocess(img):
        if len(img.shape) == 3 and img.shape[2] == 3:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # _, img = cv.threshold(img, 0, 255, cv.THRESH_OTSU)
        img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 21, 10)
        return img

    picture_not_processed = picture.copy()
    picture = preprocess(picture)
    template = preprocess(template)

    if DEBUG:
        print("Processed image:")
        plt.figure(figsize=(20, 20))
        plt.imshow(picture)
        plt.show()
    
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
        matches = matches[:10000]
        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in range(len(matches))]
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                matchesMask[i]=[1,0]
        draw_params = dict(matchColor = (0,255,0),
                        singlePointColor = (255,0,0),
                        matchesMask = matchesMask,
                        flags = cv.DrawMatchesFlags_DEFAULT)
        img3 = cv.drawMatchesKnn(picture,kp1,template,kp2,matches,None,**draw_params)
        plt.imshow(img3,),plt.show()
        plt.imsave("img.png", img3, dpi=1200)

    if DEBUG:
        # print("Corected picture + template:")
        plt.figure(figsize=(20, 20))
        plt.imshow(corrected_img)
        plt.show()

    return corrected_img

def extract_form_id_content_from_image(picture: np.ndarray) -> Tuple[str, int]:
    """
    Extracts the QR code content from an image.
    Returns: the QR code, if readable, '' if nothing is found.
    """
    # We use the pyzbar module, as opencv doesn't work for big images.
    # this requires special packages:
    # https://pypi.org/project/pyzbar/
    # for fedora, use `zbar`
    try:
        qr_codes = decode(Image.fromarray(picture))

        # no qr code was found
        if len(qr_codes) == 0:
            return '', -1

        # extract qr code
        content = str(qr_codes[0].data, encoding='utf-8')

        # should start with the URL prefix
        if not content.startswith(os.environ["FORM_ID_PREFIX"]):
            logging.info(f"Received different ID begining: {content}")
            return '', -1

        # remove prefix
        id = content[len(os.environ["FORM_ID_PREFIX"]):]

        if id.find('?') == -1:
            return id, 0
        
        page_nr = int(id[id.find('?'):])
        real_id = id[:id.find('?')]
        
        if page_nr <= 0:
            logging.info(f"Received a form with the page hardcoded as {page_nr}, which should not exist!")
            return '', -1
        
        return real_id, page_nr
    except Exception as e:
        logging.info(f"Unable to extract QR code from image: {e}")
        return '', -1

def extract_question_answer_from_form(
        fixed_pages: Dict[int, np.ndarray],
        question: Union[smart_forms_types.FormTextQuestion, smart_forms_types.FormMultipleChoiceQuestion],
        squares_location: List[smart_forms_types.Square]) -> Tuple[str, List[Union[bytes, None]]]:
    """
    fixed_picture: mapping for each page of the form where we already fixed the perspective transform.
    question: question we are trying to extract.
    square_locations: location of the squares of the question we are interested in.
    Returns the result, and a list with all the squares
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

        if DEBUG:
            # draw square, for debug
            cv.rectangle(fixed_page, (x, y), (x+dx, y+dy), (0, 255, 255), thickness=2)

        # This offset makes sure we don't include any borders in the square character.
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
    allowed_characters = (
        question.allowedCharacters
        if isinstance(question, smart_forms_types.FormTextQuestion)
        else " X*+"
    )
    squares_predictions = ocr.predict_characters(squares_content, allowed_characters)

    # compute the initial answer
    answer = ["?" for i in range(len(squares_location))]
    answer_square = [None for i in range(len(squares_location))]

    # combine the extracted values with the initial values
    # we only consider the `square_nr` positions, as the others are missing
    for square_nr, square_prediction, square_content in zip(squares_nr, squares_predictions, squares_content):
        answer[square_nr] = square_prediction
        answer_square[square_nr] = pickle.dumps(square_content)

    return "".join(answer), answer_square



def extract_answer_from_form(
            pdf_form: smart_forms_types.PdfForm,
            page_to_img: Dict[int, np.ndarray]) -> \
                Tuple[smart_forms_types.FormAnswer, List[List[Union[bytes, None]]]]:
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
    answer_images = []

    for question, squares in zip(pdf_form.description.questions, pdf_form.answer_squares_location):
        question_answer, question_images = extract_question_answer_from_form(page_to_img_fixed, question, squares)
        answers.append(question_answer)
        answer_images.append(question_images)


    form_answer = smart_forms_types.FormAnswer(
        answerId="",
        formId=pdf_form.description.formId,
        userId="",
        answers=answers,
        authorEmail=""
    )

    return form_answer, answer_images
