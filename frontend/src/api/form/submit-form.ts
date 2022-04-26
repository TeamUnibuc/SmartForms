import { FormAnswers, FormDescription } from "../models";

interface RawFormAnswer
{
  answerId: string
  formId: string
  authorEmail: string
  answers: string[]
}

type RawInferenceResponse = RawFormAnswer[]

export const Submit = async(formData: any):
                          Promise<FormAnswers[]> =>
{
  const data = await fetch('/api/inference', {
    method: "POST",
    headers:{
        'Content-Type': 'multipart/form-data'
    },
    body: formData
  })
  const content = await data.json() as RawInferenceResponse;

  console.log(content)

  return content.map(fa => {
    return {answers: fa.answers.map(stuff => {
      return {content: stuff}
    })}
  });
}
