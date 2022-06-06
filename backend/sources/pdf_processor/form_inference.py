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
    return extract_answer_from_images(images)

def extract_answer_from_images(images: List[np.ndarray]) -> \
        Optional[Tuple[smart_forms_types.FormAnswer, List[List[Union[bytes, None]]]]]:
    """
    Extracts a single answer, whose pages are in `images`.
    """
    # TODO: Do this in a try-catch block

    # images, joined with their id
    id_to_img = dict()
    form_id = ''

    for img in images:
        id = form_extractor.extract_form_id_content_from_image(img)
        if id == '':
            logging.debug("Unable to extract QR code content! Skipping file...")
        else:
            id_to_img[id] = img
            form_id = (id if id.find("?") == -1 else id[:id.find("?")])

    logging.debug(f"Found form #{form_id} from images.")

    if form_id == '':
        return None

    # retrieve form from database
    pdf_form = database.get_form_by_id(form_id)

    # try to reconstruct images
    page_to_img = dict()

    for page in range(len(pdf_form.pdf_file.pages)):
        page_id = form_id
        # TODO: Maybe some common way to fix this with the form creator?
        if page != 0:
            page_id += f"?page={page+1}"
        if page_id in id_to_img:
            page_to_img[page] = id_to_img[page_id]

    try:
        return form_extractor.extract_answer_from_form(pdf_form, page_to_img)
    except Exception as e:
        logging.warning(f"Unable to extract form: {e}")
        return None

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
        answer_from_images = extract_answer_from_images(images)
    except:
        pass
    if answer_from_images is not None:
        answers.append(answer_from_images)

    return answers
