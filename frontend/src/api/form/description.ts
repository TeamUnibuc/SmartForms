import { FormDescription } from "../models";
import fetchWrapper from "../wrapper";

export const Description = async(formId: string): Promise<FormDescription> =>
{
  const data = await fetch(`/api/form/description/${formId}`, {
    method: "GET",
    headers:{
        'Content-Type': 'application/json'
    }
  })
  return fetchWrapper(data)
}
