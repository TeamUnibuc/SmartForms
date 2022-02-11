# ENCODER SETTINGS

# height of the A4 PDF, in milimeters
PDF_H = 297
PDF_W = 210


# set dimensions for PDF markers and offesets
MARKER_PDF_OFFSET = 8
QR_CODE_SIZE = 30
BORDER_UP_LEFT_IMAGE_LOCATION = "../data/assets/border_ul.png"
BORDER_DOWN_LEFT_IMAGE_LOCATION = "../data/assets/border_dl.png"
BORDER_DOWN_RIGHT_IMAGE_LOCATION = "../data/assets/border_dr.png"
BORDER_IMAGE_SIZE = 30

# set dimension for the maximal width of the title on the PDF
MAX_PDF_TITLE_WIDTH = 100

# settings for the questions
PDF_QUESTION_TITLE_AFTER_OFFSET = 1
PDF_QUESTION_BETWEEN_OFFSET = 7
PDF_QUESTION_TITLE_LEFT_PADDING = 14
PDF_QUESTION_TITLE_MAX_LENGTH = 170

PDF_DETAILS_AFTER_OFFSET = -2
PDF_DETAILS_BETWEEN_OFFSET = 5
PDF_DETAILS_LEFT_PADDING = 15
PDF_DETAILS_MAX_LENGTH = 170

PDF_SQUARES_AFTER_OFFSET = 20
PDF_SQUARES_LEFT_PADDING = 15
PDF_SQUARES_SIZE = 8
PDF_SQUARES_MAX_LENGTH = 150 # TODO

PDF_TITLE_X_POSITION = 35
PDF_TITLE_Y_POSITION = 45

PDF_INITIAL_QUESTION_HEIGHT = 70
PDF_MAXIMAL_QUESTION_HEIGHT = 250

# Settings for the fonts
TITLE_FONT = "helvetica"
TITLE_FONT_SIZE = 36

QUESTION_TITLE_FONT = "helvetica"
QUESTION_TITLE_FONT_SIZE = 20

QUESTION_DETAILS_FONT = "helvetica"
QUESTION_DETAILS_FONT_SIZE = 15


# DECODER SETTINGS

MARKER_MATCHING_TOLERANCE = 1.3
IMAGE_BLACK_THRESHOLD = 60
POLYGON_APROXIMATION_EPSILON = 0.03