import fetchWrapper from "../wrapper"

export const Delete = async(formId: string): Promise<any> =>
{
  const data = await fetch(`/api/form/delete/${formId}`, {
    method: "DELETE",
    headers:{
        'Content-Type': 'application/json'
    }
  })
  return fetchWrapper(data, "json", "text")
}
