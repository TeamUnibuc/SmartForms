import { FormDescription } from "../models";

interface CreateResults {
  formId: string,
  formPdfBase64: string,
}

export const FormCreate = async(reqBody: FormDescription): Promise<CreateResults> =>
{
  const data = await fetch('/api/form/create', {
    method: "POST",
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(reqBody)
  })
  const content = await data.json();
  return content;
}
