from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel
import pickle
from datetime import datetime

class FormTextQuestion(BaseModel):
    """
        Stores a single text question.
    """
    title: str
    description: str
    maxAnswerLength: int
    # TODO: Consider this in OCR
    allowedCharacters: Optional[str] = ""

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
    formId: Optional[str] = ""
    description: Optional[str] = "Description of the form..."
    questions: List[Union[FormMultipleChoiceQuestion, FormTextQuestion]]
    canBeFilledOnline: bool
    needsToBeSignedInToSubmit: bool
    authorEmail: Optional[str] = ""
    creationDate: Optional[datetime]

class FormAnswer(BaseModel):
    """
        Stores a single answer to a form.
    """
    answerId: Optional[str] = ""
    formId: str
    # author email is generated based on the
    # signed user, if signed in.
    authorEmail: Optional[str] = ""
    answers: List[str]
    creationDate: Optional[datetime]

    # def to_dict(self) -> dict:
    #     return {
    #         "formId": self.formId,
    #         "answerId": self.answerId,
    #         "authorEmail": self.authorEmail,
    #         "content": pickle.dumps(self)
    #     }

# def form_answer_from_dict(d: dict) -> FormAnswer:
#     return pickle.loads(d["content"])
    