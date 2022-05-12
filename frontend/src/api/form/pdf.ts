import fetchWrapper from "../wrapper";

interface PdfResp
{
  formPdfBase64: string
}

export const Pdf = async(formId: string): Promise<PdfResp> =>
{
  const data = await fetch(`/api/form/pdf/${formId}`, {
      method: "GET",
      headers:{
          'Content-Type': 'application/json'
      }
  })
  return fetchWrapper(data)
}
