import { FormDescription } from "../models";

interface GetFormListParams {
  offset: number
  count: number
  isOwner: boolean
}

interface GetFormListResults {
  forms: FormDescription[]
}

export const FormList = async(reqBody: GetFormListParams): Promise<GetFormListResults> =>
{
  const data = await fetch('/api/form/list', {
      method: "POST",
      headers:{
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(reqBody)
  })
  const content = await data.json();
  return content;
}
