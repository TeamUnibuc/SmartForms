import logging
from typing import List, Tuple
import fpdf
import qrcode
import random
from .constants import *
import smart_forms_types.pdf_form as pdf_form
import smart_forms_types
import cv2 as cv
import tempfile


def add_square_grid_corners(pdf: fpdf.FPDF):
    """
    Adds 3 borders (not up-right, which is the QR code) in the pdf file.
    """

    def random_populate_with_squares(X, Y, SQUARE_SIZE: float, PARTITION: int, consider):
        """
        Random populate the square with corners at (X, Y) and size SQUARE_SIZE with and
        PARTITIONxPARTITION grid of small squares (black or white).
        consider(i, j) tells if we have to try to add square (i, j)
        """
        sq_offset = SQUARE_SIZE / PARTITION
        for i in range(PARTITION):
            for j in range(PARTITION):
                if consider(i, j) and random.random() < SQUARE_GRID_BLACK_SQUARE_PROBABILITY:
                    pdf.rect(
                        X + sq_offset * i,
                        Y + sq_offset * j,
                        w=sq_offset,
                        h=sq_offset,
                        style='F'
                    )

    # top left
    random_populate_with_squares(
        PDF_BORDER_OFFSET,
        PDF_BORDER_OFFSET,
        BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_SQUARE,
        lambda x, y: x < BORDER_SHORT_EDGE_SQUARE or y < BORDER_SHORT_EDGE_SQUARE   
    )

    # bottom left
    random_populate_with_squares(
        PDF_BORDER_OFFSET,
        PDF_H - PDF_BORDER_OFFSET - BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_SQUARE,
        lambda x, y: x < BORDER_SHORT_EDGE_SQUARE or (BORDER_LONG_EDGE_SQUARE - y) < BORDER_SHORT_EDGE_SQUARE   
    )

    # bottom right
    random_populate_with_squares(
        PDF_W - PDF_BORDER_OFFSET - BORDER_LONG_EDGE_PX,
        PDF_H - PDF_BORDER_OFFSET - BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_SQUARE,
        lambda x, y: (BORDER_LONG_EDGE_SQUARE - x) < BORDER_SHORT_EDGE_SQUARE or (BORDER_LONG_EDGE_SQUARE - y) < BORDER_SHORT_EDGE_SQUARE   
    )

    # left margin
    random_populate_with_squares(
        PDF_BORDER_OFFSET,
        (PDF_H - BORDER_LONG_EDGE_PX) / 2,
        BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_SQUARE,
        lambda x, y: x < BORDER_SHORT_EDGE_SQUARE
    )
    
    # right margin
    random_populate_with_squares(
        PDF_W - PDF_BORDER_OFFSET - BORDER_SHORT_EDGE_PX,
        (PDF_H - BORDER_LONG_EDGE_PX) / 2,
        BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_SQUARE,
        lambda x, y: x < BORDER_SHORT_EDGE_SQUARE
    )

def create_pdf_with_borders(data: str = '') -> fpdf.FPDF:
    """Creates an empty PDF form, with the
    appropriate markings.
    """
    # Default settings (A4, mm)
    # A4 size: 210 x 297 mm
    pdf = fpdf.FPDF()
    pdf.add_page()

    # set fill to black
    pdf.set_fill_color(0)

    # add the 3 corners
    add_square_grid_corners(pdf)
    
    # upper-right (QR code)
    # TODO: Check if this is ok (temp file leak)
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
        PDF_W - PDF_BORDER_OFFSET - QR_CODE_SIZE,
        PDF_BORDER_OFFSET,
        QR_CODE_SIZE,
        QR_CODE_SIZE
    )
    return pdf

def add_text_to_pdf(
    pdf: fpdf.FPDF, text: str, x_min, x_max, starting_y,
    font, size, style, text_height, align='L') -> float:
    """
    Prints a multiline text to the pdf, starting at height starting_y.
    text: text to print
    font, size, style: font, size and styling given to fpdf
    x_min, x_max: left-right intervals we can print to.
    text_height, align: vertical size and alignment
    returns: current height value (new starting_y)
    """
    # check http://www.fpdf.org/en/doc/multicell.htm
    # set styling 
    pdf.set_font(font, size=size, style=style)

    # split into lines
    lines = pdf.multi_cell(
        w=x_max-x_min,
        h=text_height,
        txt=text,
        align=align,
        split_only=True
    )

    # render each line
    for line in lines:
        pdf.set_xy(x_min, starting_y)
        pdf.cell(x_max - x_min, text_height, line, align=align)
        starting_y += text_height
    return starting_y

def add_title_to_pdf(pdf: fpdf.FPDF, title: str):
    """
    Adds a title to our PDF file
    pdf: our PDF file
    title: the title we have to add to the PDF
    Returns the height we can start puting questions at.
    """
    return add_text_to_pdf(
        pdf,
        title,
        PDF_TITLE_X_POSITION, PDF_W - PDF_BORDER_OFFSET - QR_CODE_SIZE - 5,
        PDF_TITLE_Y_POSITION,
        TITLE_FONT, TITLE_FONT_SIZE, '', 13, 'C'
    ) + 5

def add_answer_squares(pdf: fpdf.FPDF, current_height, count: int) -> Tuple[float, List[pdf_form.Square]]:
    """
    Adds `count` answer squares to the PDF.
    If we can't add them on a single line, they are split into multiple lines.
    returns (current height, squares)
    """
    squares = []
    
    x_act = PDF_ANSWER_SQUARE_X_MIN

    # add each 
    for i in range(count):
        # have to go to new line
        if x_act + PDF_ANSWER_SQUARE_SIZE > PDF_ANSWER_SQUARE_X_MAX:
            current_height += PDF_ANSWER_SQUARE_SIZE + 1
            x_act = PDF_ANSWER_SQUARE_X_MIN

        # add the square
        pdf.rect(x_act, current_height, PDF_ANSWER_SQUARE_SIZE, PDF_ANSWER_SQUARE_SIZE)
        squares.append(pdf_form.Square(x_act, current_height, PDF_ANSWER_SQUARE_SIZE))
        x_act += PDF_ANSWER_SQUARE_SIZE + 1

    # new line
    current_height += PDF_ANSWER_SQUARE_SIZE + 1

    return current_height, squares


def add_question_description(pdf: fpdf.FPDF, starting_height: int, question: str, details: str) -> float:
    """
    Adds the title and the description of a question.
    Used by both the text question and multiple choice question.
    returns: Starting height of the next objects
    """

    # offset between different items of the form
    current_height = starting_height

    # question title
    current_height = add_text_to_pdf(
        pdf,
        text=question,
        x_min=PDF_BORDER_OFFSET+BORDER_SHORT_EDGE_PX+5,
        x_max=PDF_W-(PDF_BORDER_OFFSET+BORDER_SHORT_EDGE_PX+5),
        starting_y=current_height,
        font=QUESTION_TITLE_FONT,
        size=QUESTION_TITLE_FONT_SIZE,
        style='',
        text_height=PDF_QUESTION_BETWEEN_OFFSET
    )
    current_height += PDF_QUESTION_TITLE_AFTER_OFFSET

    # question description
    current_height = add_text_to_pdf(
        pdf,
        text=details,
        x_min=PDF_BORDER_OFFSET+BORDER_SHORT_EDGE_PX+5,
        x_max=PDF_W-(PDF_BORDER_OFFSET+BORDER_SHORT_EDGE_PX+5),
        starting_y=current_height,
        font=QUESTION_DETAILS_FONT,
        size=QUESTION_DETAILS_FONT_SIZE,
        style='I',
        text_height=PDF_DETAILS_BETWEEN_OFFSET
    )
    current_height += PDF_DETAILS_AFTER_OFFSET

    return current_height

def add_text_question(pdf: fpdf.FPDF, starting_height: int, question: str, details: str, answer_length: int) -> Tuple[int, List[pdf_form.Square]]:
    """
    Adds a question to the PDF

    Arguments:
        pdf: pdf file we are playing with
        starting_height: height of the question in the page
        question: actual question
        details: explanation of the question
        answer_length: number of characters for the answer

    Returns: starting height for the next question
    """

    # offset between different items of the form
    current_height = starting_height

    # add title and description
    current_height = add_question_description(
        pdf,
        current_height,
        question,
        details
    )

    # display the answer space
    current_height, squares = add_answer_squares(
        pdf,
        current_height,
        answer_length
    )
    current_height += PDF_SQUARES_AFTER_OFFSET

    return current_height, squares



def add_multiple_choice_question(pdf: fpdf.FPDF, starting_height: int, question: str, details: str, choices: List[str]) -> Tuple[int, List[pdf_form.Square]]:
    """Adds a multiple choice question to the PDF

    Arguments:
        pdf -- pdf file we are playing with
        starting_height -- height of the question in the page
        question -- actual question
        details -- explanation of the question
        choices -- choices for the question

    Returns:
        int -- starting height for the next question
    """

    # offset between different items of the form
    current_height = starting_height

    # add title and description
    current_height = add_question_description(
        pdf,
        current_height,
        question,
        details
    )

    # display the answer space
    squares = []
    for choice in choices:
        square_imposed_min_height, [square] = add_answer_squares(pdf, current_height, 1)

        # move a litle bit down to center the text to the squares
        current_height += 2

        # write choice
        text_imposed_min_height = add_text_to_pdf(
            pdf,
            text=choice,
            x_min=PDF_ANSWER_SQUARE_X_MIN + PDF_ANSWER_SQUARE_SIZE + 2,
            x_max=PDF_W-(PDF_BORDER_OFFSET+BORDER_SHORT_EDGE_PX+5),
            starting_y=current_height,
            font=QUESTION_MULTIPLE_CHOICE_OPTION_FONT,
            size=QUESTION_MULTIPLE_CHOICE_OPTION_FONT_SIZE,
            style='',
            text_height=QUESTION_MULTIPLE_CHOICE_OPTION_BETWEEN_SIZE
        )

        # we have to move down by at least one square
        current_height = max(square_imposed_min_height, text_imposed_min_height)
        squares.append(square)

    current_height += PDF_SQUARES_AFTER_OFFSET

    return (current_height, squares)


def create_form_from_description(description: smart_forms_types.FormDescription) -> pdf_form.PdfForm:
    # set an id if not existent
    if description.formId == '':
        description.formId = "https://smartforms.ml/view_form/form-#" + str(random.randint(10**10, 2*10**10))

    form = pdf_form.PdfForm()
    form.description = description
    form.pdf_file = create_pdf_with_borders(description.formId)
    form.answer_squares_location = []

    # set title
    current_height = add_title_to_pdf(form.pdf_file, description.title)

    for question in description.questions:
        # check if the question is a text question
        # or a mutiple choice question
        if isinstance(question, smart_forms_types.FormTextQuestion):
            current_height, answer_squares = add_text_question(
                form.pdf_file,
                current_height,
                question.title,
                question.description,
                question.maxAnswerLength
            )
            form.answer_squares_location.append(answer_squares)
        elif isinstance(question, smart_forms_types.FormMultipleChoiceQuestion):
            current_height, answer_squares = add_multiple_choice_question(
                form.pdf_file,
                current_height,
                question.title,
                question.description,
                question.choices
            )
            form.answer_squares_location.append(answer_squares)

        # TODO: Handle multiple pages
        if current_height > PDF_MAXIMAL_PAGE_HEIGHT:
            raise Exception("There are too many questions on the form!")

    return form
