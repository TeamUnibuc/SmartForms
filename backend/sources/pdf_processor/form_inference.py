from collections import defaultdict
import numpy as np
import pdf2image
from typing import Dict, Optional, Tuple, List, Union
import logging
from PIL import Image
import cv2 as cv
import database
import smart_forms_types
import zipfile
import io
import pdf_processor.form_extractor as form_extractor

def extract_answer_from_pdf_file(pdf_file: Tuple[bytes, str]) -> Optional[Tuple[smart_forms_types.FormAnswer, List[List[Union[bytes, None]]]]]:
    """
    Extracts the content of a form within a PDF file.
    A SINGLE FORM CAN BE INCLUDED IN THE PDF FILE.
    """
    # individually extract each page of the pdf
    images = pdf2image.convert_from_bytes(pdf_file[0])
    images = [np.array(image) for image in images]

    # process pdf as list of images
    return extract_answers_from_images(images)

def extract_single_answer_from_images(images: List[Tuple[np.ndarray, str, int]]) -> \
        Optional[Tuple[smart_forms_types.FormAnswer, List[List[Union[bytes, None]]]]]:
    """
    Extracts a single answer from a list of images, all of which belong
    TO THE SAME form.
    """
    if len(images) == 0:
        return None

    try:
        pdf_form = database.get_form_by_id(images[0][1])
    except:
        logging.info(f"Unable to find form #{images[0][1]}!")
        return None
    
    page_to_img = dict()
    for img, id, page in images:
        page_to_img[page] = img
    
    try:
        return form_extractor.extract_answer_from_form(pdf_form, page_to_img)
    except Exception as e:
        logging.warning(f"Unable to extract form: {e}")
        return None


def extract_answers_from_images(images: List[np.ndarray]) -> \
        List[Tuple[smart_forms_types.FormAnswer, List[List[Union[bytes, None]]]]]:
    """
    Extracts a list of answers, whose pages are in `images`.
    This does:
      For each page, check if it is following the previous stack of pages.
            If yes, append it
            If not, start a new stack
    """
    # all of the answers we extracted
    answers = []
    # pages, with their form ID and their page nr
    current_pages: List[Tuple[np.ndarray, str, int]] = []

    def flush_current_pages():
        """
        Flushes the content of current_pages into an answer
        """
        nonlocal answers, current_pages
        try:
            answer = extract_single_answer_from_images(current_pages)
            if answer is not None:
                answers.append(answer)
        except Exception as e:
            logging.info(f"Unable to extract answer: {e}")
        current_pages = []

    for img in images:
        id, page = form_extractor.extract_form_id_content_from_image(img)
        if current_pages != [] and (current_pages[-1][1] != id or current_pages[-1][2] >= page):
            flush_current_pages()
        current_pages.append((img, id, page))
    flush_current_pages()
    
    return answers


def extract_answer_from_zip_file(zip_file: Tuple[bytes, str]) -> List[Tuple[smart_forms_types.FormAnswer, List[List[Union[bytes, None]]]]]:
    """
    Extracts the content of a zip file and processes each folder as an independent
    list of files (pdfs, images or other zips).
    """
    # files stored in each directory
    files_per_folder: Dict[str, Tuple[bytes, str]] = defaultdict(lambda: [])

    # zip object
    zip = zipfile.ZipFile(io.BytesIO(zip_file[0]))

    for filename in zip.namelist():
        file_content = zip.read(filename)
        # folder, just skip
        if len(file_content) == 0:
            continue
        # filename starting AFTER the last '/'
        filename_without_folder = filename[max(0, filename.rfind('/') + 1):]
        # folder name
        folder_name = filename[:len(filename) - len(filename_without_folder)]

        # save the file in the apropriate directory
        files_per_folder[folder_name].append((file_content, filename))

    # stores all of the answers from within the zip file
    answers = []

    # process each folder independently
    for folder_name in files_per_folder:
        answers += extract_answers_from_files(files_per_folder[folder_name])

    return answers

def extract_answers_from_files(files: List[Tuple[bytes, str]]) -> List[Tuple[smart_forms_types.FormAnswer, List[List[Union[bytes, None]]]]]:
    """
    Processes files, extracting their answers.
    The files have to be an image, a pdf or a zip.
    """

    # all of the answers processed until now
    answers = []

    # here we store all of the images in our current scope
    images: List[np.ndarray] = []

    logging.info("extracting files")
    # process each file
    for file_content, filename in files:
        if filename.endswith(".pdf"):
            pdf_content = extract_answer_from_pdf_file((file_content, filename))
            if pdf_content is not None:
                answers.append(pdf_content)
        elif filename.endswith(".zip"):
            answers += extract_answer_from_zip_file((file_content, filename))
        else:
            # try to read as image
            try:
                image = Image.open(io.BytesIO(file_content))
                image = np.array(image)
                images.append(image)
            except:
                pass
    
    # add the answer from the images, if it exists
    answer_from_images = None
    try:
        answer_from_images = extract_answers_from_images(images)
    except:
        pass
    if answer_from_images is not None:
        answers += answer_from_images

    return answers
