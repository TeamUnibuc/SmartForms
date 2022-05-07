import { AllFormEntries, APIError, FormAnswers, HTTPValidationError } from "../models";

interface VFEBody
{
  formId: string
  offset: number
  count: number
}

const transformMChoice = (ans: FormAnswers) =>
{
  return {
    ...ans,
    answers: ans.answers.map(x => x.content)
  }
}

export const ViewFormEntries = async(reqBody: VFEBody): Promise<AllFormEntries> =>
{
  const data = await fetch('/api/entry/view-form-entries', {
    method: "POST",
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(reqBody)
  })
  if (data.status !== 200) {
    console.log("Status not 200")
    const err: APIError<string | HTTPValidationError> = {
      statusCode: data.status,
      data: await data.text()
    }
    throw err
  }
  const content = await data.json()
  return content;
}
