import { APIError, FormAnswers, HTTPValidationError, SingleQAnswer } from "../models";
import fetchWrapper from "../wrapper";

interface CreateProps
{
  formId: string
  answers: SingleQAnswer[]
}

const transformMChoice = (ans: FormAnswers) =>
{
  return {
    ...ans,
    answers: ans.answers.map(x => x.content)
  }
}

export const Create = async(reqBody: CreateProps): Promise<string> =>
{
  const data = await fetch('/api/entry/create', {
    method: "POST",
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(transformMChoice({
      answerId: "",
      authorEmail: "",
      answers: reqBody.answers,
      formId: reqBody.formId,
      creationDate: ""
    }))
  })

  return fetchWrapper<string | HTTPValidationError>(data)
}
