from locale import Error
from typing import List, Tuple
import fpdf
import qrcode
import random
from .constants import *
import os
import internal_types.pdf_form as pdf_form
import routers.models as models

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

    # upper-left corner
    pdf.rect(
        MARKER_PDF_OFFSET,
        MARKER_PDF_OFFSET,
        MARKER_SMALL_SIDE,
        MARKER_LARGE_SIDE,
        style='F'
    )
    pdf.rect(
        MARKER_PDF_OFFSET,
        MARKER_PDF_OFFSET,
        MARKER_LARGE_SIDE,
        MARKER_SMALL_SIDE,
        style='F'
    )

    # upper-right (QR code)
    file_name = "/tmp/smart-forms-img-" + str(random.randint(0, 10**10)) + ".png"
    qr_code_maker = qrcode.QRCode(
        border=0
    )
    qr_code_maker.add_data(data)
    qr_code_maker.make(fit=True)
    qr_code = qr_code_maker.make_image()
    qr_code.save(file_name)

    pdf.image(
        file_name,
        PDF_W - MARKER_PDF_OFFSET - QR_CODE_SIZE,
        MARKER_PDF_OFFSET,
        QR_CODE_SIZE,
        QR_CODE_SIZE
    )
    os.remove(file_name)

    # # down-left
    # pdf.rect(
    #     MARKER_PDF_OFFSET,
    #     PDF_H - MARKER_PDF_OFFSET - MARKER_LARGE_SIDE,
    #     MARKER_SMALL_SIDE,
    #     MARKER_LARGE_SIDE,
    #     style='F'
    # )
    # pdf.rect(
    #     MARKER_PDF_OFFSET,
    #     PDF_H - MARKER_PDF_OFFSET - MARKER_SMALL_SIDE,
    #     MARKER_LARGE_SIDE,
    #     MARKER_SMALL_SIDE,
    #     style='F'
    # )

    # # down-right
    # pdf.rect(
    #     PDF_W - MARKER_PDF_OFFSET - MARKER_SMALL_SIDE,
    #     PDF_H - MARKER_PDF_OFFSET - MARKER_LARGE_SIDE, 
    #     MARKER_SMALL_SIDE,
    #     MARKER_LARGE_SIDE,
    #     style='F'
    # )
    # pdf.rect(
    #     PDF_W - MARKER_PDF_OFFSET - MARKER_LARGE_SIDE,
    #     PDF_H - MARKER_PDF_OFFSET - MARKER_SMALL_SIDE,
    #     MARKER_LARGE_SIDE,
    #     MARKER_SMALL_SIDE,
    #     style='F'
    # )
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


def create_form_from_description(description: models.FormDescription) -> pdf_form.PdfForm:
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
        if isinstance(question, models.FormTextQuestion):
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