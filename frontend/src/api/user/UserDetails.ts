export interface UserDetails {
  is_signed_in: boolean
  email: string
  full_name: string
  given_name: string
  family_name: string
  picture: string
}

export const GetUserDetails = async(): Promise<undefined | UserDetails> =>
{
  try {
    const data = await fetch('/api/user/details', {
      method: "GET",
      headers:{
          'Content-Type': 'application/json'
      }
    })
    const content = await data.json() as UserDetails;
    return content;
  }
  catch (err) {
    console.log("Error fetching user status, maybe not logged in?")
    return undefined
  }
}
