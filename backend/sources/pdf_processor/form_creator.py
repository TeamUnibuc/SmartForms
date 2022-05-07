import logging
import os
from typing import List, Tuple
import fpdf
import qrcode
import random

from .constants import *
import smart_forms_types.pdf_form as pdf_form
import smart_forms_types
import cv2 as cv
import tempfile

class FormCreatorParameters:
    """
    Parameters passed around while creating the PDF.
    """
    form_title: str
    is_preview: bool
    def __init__(self, form_title, is_preview):
        self.form_title = form_title
        self.is_preview = is_preview

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
        lambda x, y: x < BORDER_SHORT_EDGE_SQUARE or (BORDER_LONG_EDGE_SQUARE - y) <= BORDER_SHORT_EDGE_SQUARE   
    )

    # bottom right
    random_populate_with_squares(
        PDF_W - PDF_BORDER_OFFSET - BORDER_LONG_EDGE_PX,
        PDF_H - PDF_BORDER_OFFSET - BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_PX,
        BORDER_LONG_EDGE_SQUARE,
        lambda x, y: (BORDER_LONG_EDGE_SQUARE - x) <= BORDER_SHORT_EDGE_SQUARE or (BORDER_LONG_EDGE_SQUARE - y) <= BORDER_SHORT_EDGE_SQUARE   
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

#TODO: change this name
def add_borders_to_page(pdf: fpdf.FPDF, qr_code_content: str = '') -> fpdf.FPDF:
    """Creates an empty PDF form, with the
    appropriate markings.
    """
    # Default settings (A4, mm)
    # A4 size: 210 x 297 mm
    # pdf.add_page()

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
    qr_code_maker.add_data(qr_code_content)
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

def add_page_if_required(pdf: fpdf.FPDF, current_height, params: FormCreatorParameters) -> float:
    """
    Adds a new page to the PDF document if the bottom of the page is reached.
    Returns the new height (unchanged if no additional pages are required).
    """
    # don't need to add new page
    if current_height <= PDF_MAXIMAL_PAGE_HEIGHT:
            return current_height

    
    pdf.add_page()

    # add "PREVIEW" watermark
    if params.is_preview:
        pdf.set_font(TITLE_FONT, size=140, style='B')
        pdf.set_xy(0, 0)
        pdf.rotate(45, PDF_W / 2, PDF_H / 2)

        pdf.set_text_color(210)
        pdf.set_xy(0, 130)
        pdf.cell(40, 20, "PREVIEW")
        pdf.set_text_color(0)

        pdf.set_xy(0, 0)
        pdf.rotate(0)

    # TODO: if not first page, make title smaller
    title = params.form_title
    if len(pdf.pages) > 1:
        title += f" - page #{len(pdf.pages)}"
    return add_title_to_pdf(pdf, title, params)


def add_text_to_pdf(
    pdf: fpdf.FPDF, text: str, x_min, x_max, starting_y,
    font, size, style, text_height, align, params) -> float:
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
        # add a new page if required.
        starting_y = add_page_if_required(pdf, starting_y, params)

        # reset the font, in case a new page was added.
        pdf.set_font(font, size=size, style=style)

        # se position and add text
        pdf.set_xy(x_min, starting_y)
        pdf.cell(x_max - x_min, text_height, line, align=align)

        # increase height
        starting_y += text_height
    return starting_y

def add_title_to_pdf(pdf: fpdf.FPDF, title: str, params: FormCreatorParameters):
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
        TITLE_FONT, TITLE_FONT_SIZE, '', 13, 'C',
        params
    ) + 5

def add_answer_squares(pdf: fpdf.FPDF, current_height, count: int, params) -> Tuple[float, List[pdf_form.Square]]:
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

        # add page if required
        current_height = add_page_if_required(pdf, current_height, params)

        # add the square
        pdf.rect(x_act, current_height, PDF_ANSWER_SQUARE_SIZE, PDF_ANSWER_SQUARE_SIZE)
        squares.append(
            pdf_form.Square(
                x=x_act,
                y=current_height,
                width=PDF_ANSWER_SQUARE_SIZE,
                page=len(pdf.pages) - 1
            )
        )
        x_act += PDF_ANSWER_SQUARE_SIZE + 1

    # new line
    current_height += PDF_ANSWER_SQUARE_SIZE + 1

    return current_height, squares


def add_question_description(pdf: fpdf.FPDF, starting_height: int, question: str, details: str, params) -> float:
    """
    Adds the title and the description of a question.
    Used by both the text question and multiple choice question.
    returns: Starting height of the next objects
    """

    # offset between different items of the form
    current_height = starting_height

    if question != "":
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
            text_height=PDF_QUESTION_BETWEEN_OFFSET,
            align='L',
            params=params
        )
        current_height += PDF_QUESTION_TITLE_AFTER_OFFSET

    if details != "":
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
            text_height=PDF_DETAILS_BETWEEN_OFFSET,
            align='L',
            params=params
        )
        current_height += PDF_DETAILS_AFTER_OFFSET

    return current_height

def add_text_question(pdf: fpdf.FPDF, starting_height: int, question: str, details: str, answer_length: int, params) -> Tuple[int, List[pdf_form.Square]]:
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
        details,
        params
    )

    # display the answer space
    current_height, squares = add_answer_squares(
        pdf,
        current_height,
        answer_length,
        params
    )
    current_height += PDF_SQUARES_AFTER_OFFSET

    return current_height, squares



def add_multiple_choice_question(pdf: fpdf.FPDF, starting_height: int, question: str, details: str, choices: List[str], params) -> Tuple[int, List[pdf_form.Square]]:
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
        details,
        params
    )

    # display the answer space
    squares = []
    for choice in choices:
        TEXT_OFFSET_FROM_SQUARES = 2

        # add a new page if required by text
        new_current_height = add_page_if_required(pdf, current_height+TEXT_OFFSET_FROM_SQUARES, params)
        # height decresed => we added a new page
        # => we will do everything on the new page
        if new_current_height < current_height:
            current_height = new_current_height

        square_imposed_min_height, [square] = add_answer_squares(pdf, current_height, 1, params)
        pages_after_adding_square = len(pdf.pages)

        # move a litle bit down to center the text to the squares
        current_height += TEXT_OFFSET_FROM_SQUARES

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
            text_height=QUESTION_MULTIPLE_CHOICE_OPTION_BETWEEN_SIZE,
            align='L',
            params=params
        )
        pages_after_adding_text = len(pdf.pages)

        # if we have more pages after text, relevant height is given by the text
        if pages_after_adding_square != pages_after_adding_text:
            current_height = text_imposed_min_height
        else:
            # we have to move down by at least one square
            current_height = max(square_imposed_min_height, text_imposed_min_height)
        
        squares.append(square)

    current_height += PDF_SQUARES_AFTER_OFFSET

    return (current_height, squares)


def create_form_from_description(description: smart_forms_types.FormDescription, is_preview: bool) -> pdf_form.PdfForm:
    # set an id if not existent
    if description.formId == '':
        raise Exception("Form should have an ID")

    params = FormCreatorParameters(description.title, is_preview)

    form = pdf_form.PdfForm(
        description=description,
        pdf_file=fpdf.FPDF(),
        answer_squares_location=[]
    )
    pdf = form.pdf_file

    # disable line breaks
    pdf.set_auto_page_break(False)

    # force a new page
    # TODO: get rid of 10**10
    current_height = add_page_if_required(pdf, 10**10, params)

    form.answer_squares_location = []

    for question in description.questions:
        # check if the question is a text question
        # or a mutiple choice question
        if isinstance(question, smart_forms_types.FormTextQuestion):
            current_height, answer_squares = add_text_question(
                pdf,
                current_height,
                question.title,
                question.description,
                question.maxAnswerLength,
                params
            )
            form.answer_squares_location.append(answer_squares)
        elif isinstance(question, smart_forms_types.FormMultipleChoiceQuestion):
            current_height, answer_squares = add_multiple_choice_question(
                pdf,
                current_height,
                question.title,
                question.description,
                question.choices,
                params
            )
            form.answer_squares_location.append(answer_squares)

    
    # add borders
    # indexed from 1

    for page_nr in range(1, len(pdf.pages) + 1):
        pdf.page = page_nr
        form_id_on_page = description.formId

        # if the page is not the first, then its ID will contain the page nr.
        if page_nr > 1:
            form_id_on_page += f"?page={page_nr}"
        add_borders_to_page(
            pdf,
            os.environ["FORM_ID_PREFIX"] + form_id_on_page
        )

        # if there are more than one page, display it
        if len(pdf.pages) > 1:
            page_info = f"Page {page_nr}/{len(pdf.pages)}"
            # TODO: change font
            # FPDF doesn't support changing pages (what we do with
            # pdf.page=xxx), so we have to force flush the settings
            # of the font.
            pdf.set_font(QUESTION_DETAILS_FONT, size=21, style="I")
            pdf.set_font(QUESTION_DETAILS_FONT, size=20, style="I")

            pdf.set_xy(
                PDF_BORDER_OFFSET + BORDER_LONG_EDGE_PX + 5,
                PDF_H - PDF_BORDER_OFFSET - BORDER_SHORT_EDGE_PX + 1.5
            )

            pdf.cell(
                PDF_W - 2 * PDF_BORDER_OFFSET - 2 * BORDER_LONG_EDGE_PX - 2 * 5,
                10,
                txt=page_info,
                align="R"
            )

    return form
