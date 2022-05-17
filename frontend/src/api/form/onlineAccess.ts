import fetchWrapper from "../wrapper"

interface OAProps
{
  canBeFilledOnline: boolean
  needsToBeSignedInToSubmit: boolean
}

export const OnlineAccess = async(formId: string, reqBody: OAProps): Promise<any> =>
{
  const data = await fetch(`/api/form/online-access/${formId}`, {
    method: "PUT",
    headers:{
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(reqBody)
  })
  return fetchWrapper(data)
}
