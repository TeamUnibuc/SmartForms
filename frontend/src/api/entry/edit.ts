import { APIError, FormAnswers, HTTPValidationError } from "../models";

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
  if (data.status !== 200) {
    const err: APIError<string | HTTPValidationError> = {
      statusCode: data.status,
      data: await data.json()
    }
    throw err
  }
  const content = await data.text()
  return content;
}
