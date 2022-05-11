import { FormDescription } from "../models";

export const Description = async(formId: string): Promise<FormDescription> =>
{
  const data = await fetch(`/api/form/description/${formId}`, {
    method: "GET",
    headers:{
        'Content-Type': 'application/json'
    }
  })
  const content = await data.json();
  console.log("api form description")
  console.log(content)
  return content;
}
