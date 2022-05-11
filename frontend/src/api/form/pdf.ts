import { FormDescription } from "../models";
import fetchWrapper from "../wrapper";

export const Pdf = async(formId: string): Promise<string> =>
{
  const data = await fetch(`/api/form/pdf/${formId}`, {
      method: "GET",
      headers:{
          'Content-Type': 'application/json'
      }
  })
  return fetchWrapper(data, "text")
}
