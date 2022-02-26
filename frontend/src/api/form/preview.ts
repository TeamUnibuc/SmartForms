import { FormDescription } from "../models";

interface PreviewResults {
  formPdfBase64: string
}

export const FormPreview = async(reqBody: FormDescription): Promise<PreviewResults> =>
{
  const data = await fetch('/api/form/preview', {
    method: "POST",
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(reqBody)
  })
  const content = await data.json();
  return content;
}
