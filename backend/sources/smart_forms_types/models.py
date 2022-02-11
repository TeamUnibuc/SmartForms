from typing import List, Optional, Union
from pydantic import BaseModel

class FormTextQuestion(BaseModel):
    """
        Stores a single text question.
    """
    title: str
    description: str
    maxAnswerLength: int

class FormMultipleChoiceQuestion(BaseModel):
    """
        Stores a multiple choice question.
    """
    title: str
    description: str
    choices: List[str]

class FormDescription(BaseModel):
    """
        Stores a single form.
    """
    title: str
    formId: str = ""
    description: str
    questions: List[Union[FormMultipleChoiceQuestion, FormTextQuestion]]
    canBeFilledOnline: bool
    needsToBeSignedInToSubmit: bool

class FormAnswer(BaseModel):
    """
        Stores a single answer to a form.
    """
    answerId: str
    formId: str
    userId: str
    answers: List[str]