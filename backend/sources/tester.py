import pdf_generator.form_creator
import routers.models

def run():
    question = routers.models.FormTextQuestion(
        title = "Intrebare",
        description = "detalii intrebare",
        maxAnswerLength = 10
    )

    desc = routers.models.FormDescription(
        title = "Titlu",
        description = "Descriere",
        canBeFilledOnline = False,
        needsToBeSignedInToSubmit = False,
        formId = "form 1234",
        questions = [question]
    )

    m = pdf_generator.form_creator.create_form_from_description(desc)

    with open("file.pdf", "wb") as fout:
        fout.write(m.extract_raw_pdf_bytes())