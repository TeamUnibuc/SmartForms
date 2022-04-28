import { FormAnswers } from "../models";

interface RawFormAnswer
{
  answerId: string
  formId: string
  authorEmail: string
  answers: string[]
}

type RawInferenceResponse = RawFormAnswer[]

export const Submit = async(formData: any):
                      Promise<string | FormAnswers[]> =>
{
  try {
    const data = await fetch('/api/inference', {
      method: "POST",
      headers:{
          'Content-Type': 'multipart/form-data'
      },
      body: formData
    })
    const content = await data.json() as RawInferenceResponse;
    console.log(content)

    if (content.map === undefined || content.length === undefined)
      throw new Error("Bad parsing")

    return content.map(fa => {
      return {
        formId: fa.formId,
        answers: fa.answers.map(stuff => {
          return {content: stuff}
        })
      }
    });
  } catch (e)
  {
    return "Error parsing document: " + (e as Error).message
  }

}
