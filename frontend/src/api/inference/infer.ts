import { FormAnswers } from "../models";

interface RawFormAnswer
{
  answerId: string
  creationDate: string
  formId: string
  authorEmail: string
  answers: string[]
}

type RawInferenceResponse =
{
  entries: RawFormAnswer[]
  errors: string[]
}
export type InferenceResponse = string | FormAnswers[]

export const Infer = async(formData: any):
                         Promise<InferenceResponse> =>
{
  try {
    const data = await fetch('/api/inference/infer', {
      method: "POST",
      body: formData

    })
    const content = await data.json() as RawInferenceResponse;
    console.log(content)

    return content.entries.map(fa => ({
        formId: fa.formId,
        answerId: fa.answerId,
        authorEmail: fa.authorEmail,
        creationDate: fa.creationDate,
        answers: fa.answers.map(stuff => {
          return {content: stuff}
        })
      })
    );
  } catch (e)
  {
    return "Error parsing document: " + (e as Error).message
  }

}
