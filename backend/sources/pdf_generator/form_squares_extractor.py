from typing import List, Tuple
from .constants import *
import numpy as np
from .squares_extractor import FormImageTransformer
import pdf_generator.database_connection as database_connection
import matplotlib.pyplot as plt


def _extract_square_from_image(image: np.ndarray, square: database_connection.Square) -> np.ndarray:
    HEIGHT_WITHOUT_BORDERS = PDF_H - 2 * MARKER_PDF_OFFSET
    WIDTH_WITHOUT_BORDERS = PDF_W - 2 * MARKER_PDF_OFFSET

    def transform_point(X: int, Y: int) -> Tuple[int, int]:
        new_x = (X - MARKER_PDF_OFFSET) / WIDTH_WITHOUT_BORDERS
        new_x *= image.shape[1]
        new_x = int(new_x)

        new_y = (Y - MARKER_PDF_OFFSET) / HEIGHT_WITHOUT_BORDERS
        new_y *= image.shape[0]
        new_y = int(new_y)
        return new_x, new_y

    x1, y1 = transform_point(square.x1, square.y1)
    x2, y2 = transform_point(square.x2, square.y2)

    # print(f"New coordonates: x1 {x1}, y1 {y1}, x2 {x2}, y2 {y2}")

    square_image = image[y1:y2+1, x1:x2+1]
    plt.imshow(square_image)
    plt.show()
    return square_image
        

def extract_squares_from_form(image: np.ndarray) -> List[List[np.ndarray]]:
    """Extracts squares containing single characters from a form.
    
    Arguments:
        form -- image of the form being processed.
        
    Returns:
        List of lines, each line being a list of single images of a character
    """
    transformer = FormImageTransformer(image)

    form_object = database_connection.retreive_form(transformer.qr_content)
    transformed_image = transformer.image_after_perspective_change
    plt.imshow(transformed_image)
    plt.show()

    answer = []
    for question in form_object.questions:
        lin = []
        for square in question.answer_squares:
            lin.append(_extract_square_from_image(transformed_image, square))

    return answer