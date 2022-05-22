
from datetime import datetime
from typing import List, Union
import smart_forms_types
import database

class InferedCharacter:
    """
    Stores information about an infered character, which
    can later be used for generating a dataset.
    """
    answerId: str
    # which question this character is part of
    questionNr: int
    # the nr of the character in the question
    characterNr: int
    # dump of the np array of the image matrix
    image: bytes
    # prediction
    prediction = str
    # when was the prediction made
    date: datetime

    def __init__(self, answerId, questionNr, characterNr, image, prediction, date):
        self.answerId = answerId
        self.questionNr = questionNr
        self.characterNr = characterNr
        self.image = image
        self.prediction = prediction
        self.date = date

    @staticmethod
    def from_dict(d: dict):
        return InferedCharacter(
            answerId=d["answerId"],
            questionNr=d["questionNr"],
            characterNr=d["characterNr"],
            image=d["image"],
            prediction=d["prediction"],
            date=d["date"]
        )

    def dict(self):
        return {
            "answerId": self.answerId,
            "questionNr": self.questionNr,
            "characterNr": self.characterNr,
            "image": self.image,
            "prediction": self.prediction,
            "date": self.date
        }

    @staticmethod
    def populate_database_from_answer(
            answer: smart_forms_types.FormAnswer,
            images: List[List[Union[bytes, None]]]):
        """
        Creates InteredCharacters objects for each character and adds
        them to the database
        """
        
        inference_characters = []

        assert len(images) == len(answer.answers)
        for question_nr in range(len(images)):
            assert len(images[question_nr]) == len(answer.answers[question_nr])
            for character_nr in range(len(images[question_nr])):
                # if the character is not None, then add it to the db
                if images[question_nr][character_nr] is not None:
                    inf_chr = InferedCharacter(
                        answer.answerId,
                        question_nr,
                        character_nr,
                        images[question_nr][character_nr],
                        answer.answers[question_nr][character_nr],
                        datetime.now()
                    )
                    inference_characters.append(inf_chr)

        if inference_characters != []:
            db = database.get_collection(database.INFERENCE_CHARACTERS)
            db.insert_many([i.dict() for i in inference_characters])

class DatasetCharacter:
    """
    Annotated character, to be used for training the NN.
    """
    image: bytes
    label = str

    def __init__(self, image, label):
        self.image = image
        self.label = label

    @staticmethod
    def from_dict(d: dict):
        return InferedCharacter(
            image=d["image"],
            label=d["label"]
        )

    def dict(self):
        return {
            "image": self.image,
            "label": self.label
        }
