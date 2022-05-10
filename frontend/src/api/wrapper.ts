import { APIError } from "./models"

const fetchWrapper = async <E = any>(
    response: Response,
    ok_ret_type: "text" | "json" = "json",
    err_ret_type: "text" | "json" = "json",
) =>
{
  if (response.status == 200) {
    return await response[ok_ret_type]()
  }
  else {
    console.log(`Fetch request code: ${response.status}`)
    const err: APIError<E> = {
      statusCode: response.status,
      data: await response[err_ret_type]()
    }
    throw err
  }
}

export default fetchWrapper
