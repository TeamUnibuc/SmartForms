import { APIError, FormAnswers, HTTPValidationError } from "../models";
import fetchWrapper from "../wrapper";

const transformMChoice = (ans: FormAnswers) =>
{
  return {
    ...ans,
    answers: ans.answers.map(x => x.content)
  }
}

export const Edit = async(reqBody: FormAnswers): Promise<string> =>
{
  const data = await fetch('/api/entry/edit', {
    method: "PUT",
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(transformMChoice(reqBody))
  })

  return fetchWrapper<string | HTTPValidationError>(data, "text")
}
