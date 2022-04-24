from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel
import pickle
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

class FormAnswer(BaseModel):
    """
        Stores a single answer to a form.
    """
    answerId: Optional[str] = ""
    formId: str
    authorEmail: str
    answers: List[str]

    def to_dict(self) -> dict:
        return {
            "formId": self.formId,
            "answerId": self.answerId,
            "userId": self.userId,
            "content": pickle.dumps(self)
        }

def form_answer_from_dict(d: dict) -> FormAnswer:
    return pickle.loads(d["content"])
    