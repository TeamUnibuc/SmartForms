from locale import Error
import logging
from typing import List, Tuple
import fpdf
import qrcode
import random
from .constants import *
import os
import smart_forms_types.pdf_form as pdf_form
import smart_forms_types
import cv2 as cv
import tempfile

def _random_populate_with_squares(pdf: fpdf.FPDF, X, Y, SQUARE_SIZE, PARTITION: int):
    """
    Random populate the square with corners at (X, Y) and size SQUARE_SIZE with and
    PARTITIONxPARTITION grid of small squares.
    """
    sq_offset = SQUARE_SIZE / PARTITION
    for i in range(PARTITION):
        for j in range(PARTITION):
            if random.random() < 0.6:
                pdf.rect(
                    X + sq_offset * i,
                    Y + sq_offset * j,
                    w=sq_offset,
                    h=sq_offset,
                    style='F'
                )

def _make_corner(pdf: fpdf.FPDF, X, Y, SIZE, border: str):
    """
    Makes a border in the pdf file.
    border is one of "up-left", "down-left", "down-right"
    """
    size = SIZE / 2
    partition = 10

    if border != "down-right":
        _random_populate_with_squares(
            pdf, X, Y, size, partition
        )
    if border != "down-left":
        _random_populate_with_squares(
            pdf, X + size, Y, size, partition
        )
    if border != "up-left":
        _random_populate_with_squares(
            pdf, X + size, Y + size, size, partition
        )
    _random_populate_with_squares(
        pdf, X, Y + size, size, partition
    )

def _create_pdf_with_borders(data: str = '') -> fpdf.FPDF:
    """Creates an empty PDF form, with the
    appropriate markings.
    """
    # Default settings (A4, mm)
    # A4 size: 210 x 297 mm
    pdf = fpdf.FPDF()
    pdf.add_page()

    # set fill to black
    pdf.set_fill_color(0)

    _make_corner(
        pdf,
        MARKER_PDF_OFFSET,
        MARKER_PDF_OFFSET,
        BORDER_IMAGE_SIZE,
        "up-left"
    )
    _make_corner(
        pdf,
        MARKER_PDF_OFFSET,
        PDF_H - MARKER_PDF_OFFSET - BORDER_IMAGE_SIZE,
        BORDER_IMAGE_SIZE,
        "down-left"
    )
    _make_corner(
        pdf,
        PDF_W - MARKER_PDF_OFFSET - BORDER_IMAGE_SIZE,
        PDF_H - MARKER_PDF_OFFSET - BORDER_IMAGE_SIZE,
        BORDER_IMAGE_SIZE,
        "down-right"
    )
    # pdf.image(
    #     BORDER_UP_LEFT_IMAGE_LOCATION,
    #     MARKER_PDF_OFFSET,
    #     MARKER_PDF_OFFSET,
    #     w=BORDER_IMAGE_SIZE,
    #     h=BORDER_IMAGE_SIZE
    # )
    # pdf.image(
    #     BORDER_DOWN_LEFT_IMAGE_LOCATION,
    #     MARKER_PDF_OFFSET,
    #     PDF_H - MARKER_PDF_OFFSET - BORDER_IMAGE_SIZE,
    #     w=BORDER_IMAGE_SIZE,
    #     h=BORDER_IMAGE_SIZE
    # )
    # pdf.image(
    #     BORDER_DOWN_RIGHT_IMAGE_LOCATION,
    #     PDF_W - MARKER_PDF_OFFSET - BORDER_IMAGE_SIZE,
    #     PDF_H - MARKER_PDF_OFFSET - BORDER_IMAGE_SIZE,
    #     w=BORDER_IMAGE_SIZE,
    #     h=BORDER_IMAGE_SIZE
    # )

    # upper-right (QR code)
    filename = None
    with tempfile.NamedTemporaryFile(suffix='.png') as temp_file:
        filename = temp_file.name
    logging.debug(f"Logging temp filename: {filename}")
    
    qr_code_maker = qrcode.QRCode(
        border=0
    )
    qr_code_maker.add_data(data)
    qr_code_maker.make(fit=True)
    qr_code = qr_code_maker.make_image()
    qr_code.save(filename)

    pdf.image(
        temp_file.name,
        PDF_W - MARKER_PDF_OFFSET - QR_CODE_SIZE,
        MARKER_PDF_OFFSET,
        QR_CODE_SIZE,
        QR_CODE_SIZE
    )
    return pdf

def _add_title_to_pdf(pdf: fpdf.FPDF, title: str):
    """Adds a title to our PDF file

    Arguments:
        pdf -- our PDF file
        title -- the title we have to add to the PDF
    """
    pdf.set_font(TITLE_FONT, size=TITLE_FONT_SIZE)
    title_lines = pdf.multi_cell(MAX_PDF_TITLE_WIDTH, 45, title, split_only=True)
    if len(title_lines) > 1:
        raise Error("The title choosen is too long!")

    pdf.text(PDF_TITLE_X_POSITION, PDF_TITLE_Y_POSITION, title)

def _add_answer_squares(pdf: fpdf.FPDF, x: int, y: int, count: int) -> List[pdf_form.Square]:
    if PDF_SQUARES_MAX_LENGTH < count:
        raise Error(f"Asked to add {count} squares, but max allowed is {PDF_SQUARES_MAX_LENGTH}!")
    squares = []
    for i in range(count):
        pdf.rect(x, y, PDF_SQUARES_SIZE, PDF_SQUARES_SIZE)
        squares.append(pdf_form.Square(x, y, PDF_SQUARES_SIZE))
        x += PDF_SQUARES_SIZE + 1

    return squares

def _add_question(pdf: fpdf.FPDF, starting_height: int, question: str, details: str, answer_length: int) -> Tuple[int, List[pdf_form.Square]]:
    """Adds a question to the PDF

    Arguments:
        pdf -- pdf file we are playing with
        starting_height -- height of the question in the page
        question -- actual question
        details -- explanation of the question
        answer_length -- number of characters for the answer

    Returns:
        int -- starting height for the next question
    """

    # offset between different items of the form
    current_height = starting_height

    # display the question
    pdf.set_font(QUESTION_TITLE_FONT, size=QUESTION_TITLE_FONT_SIZE)
    # split into lines
    title_lines = pdf.multi_cell(
        PDF_QUESTION_TITLE_MAX_LENGTH,
        PDF_QUESTION_BETWEEN_OFFSET,
        question,
        split_only=True
    )
    for title_line in title_lines:
        pdf.text(PDF_QUESTION_TITLE_LEFT_PADDING, current_height, title_line)
        current_height += PDF_QUESTION_BETWEEN_OFFSET
    current_height += PDF_QUESTION_TITLE_AFTER_OFFSET

    # display the details
    pdf.set_font(QUESTION_DETAILS_FONT, style='I', size=QUESTION_DETAILS_FONT_SIZE)
    details_lines = pdf.multi_cell(
        PDF_DETAILS_MAX_LENGTH,
        PDF_DETAILS_BETWEEN_OFFSET,
        details,
        split_only=True
    )

    for details_line in details_lines:
        pdf.text(PDF_DETAILS_LEFT_PADDING, current_height, details_line)
        current_height += PDF_DETAILS_BETWEEN_OFFSET
    current_height += PDF_DETAILS_AFTER_OFFSET

    # display the answer space
    squares = _add_answer_squares(pdf, PDF_SQUARES_LEFT_PADDING, current_height, answer_length)
    current_height += PDF_SQUARES_AFTER_OFFSET

    return (current_height, squares)


def create_form_from_description(description: smart_forms_types.FormDescription) -> pdf_form.PdfForm:
    # set an id if not existent
    if description.formId == '':
        description.formId = "form-#" + str(random.randint(10**10, 2*10**10))

    form = pdf_form.PdfForm()
    form.description = description
    form.pdf_file = _create_pdf_with_borders(description.formId)
    form.answer_squares_location = []

    # set title
    _add_title_to_pdf(form.pdf_file, description.title)

    current_height = PDF_INITIAL_QUESTION_HEIGHT

    for question in description.questions:
        # for now we only process text questions
        # TODO: non-text questions
        if isinstance(question, smart_forms_types.FormTextQuestion):
            current_height, answer_squares = _add_question(
                form.pdf_file,
                current_height,
                question.title,
                question.description,
                question.maxAnswerLength
            )
            form.answer_squares_location.append(answer_squares)
        else:
            raise NotImplementedError("Multiple description not implemented yet!")

        if current_height > PDF_MAXIMAL_QUESTION_HEIGHT:
            raise Error("There are too many questions on the form!")

    return form
