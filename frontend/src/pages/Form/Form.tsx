import { Box, Alert, Typography } from "@mui/material"
import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import API from "~/api"
import { FormDescription } from "~/api/models"

const FormPage = () =>
{
  const [searchParams, _setSearchParams] = useSearchParams()
  const [formData, setFormData] = useState<undefined | FormDescription>()
  const [loading, setLoading] = useState(true)

  const formId = searchParams.get("formId")

  useEffect(() => {
    const getter = async () => {
      await API.Form.Description(formId || "idiot")
        .then(r => setFormData(r))
        .catch(e => console.log(`Error getting formId: ${e}`))
        .finally(() => setLoading(false))
    }

    getter()
  }, [])

  if (loading)
    return <Alert severity="info"><Typography>Loading ...</Typography></Alert>

  if (formData === undefined)
    return <Alert severity={"error"}> Could not find form :/ </Alert>

  console.log(formData)

  // TODO: Put more info about the form
  return <Box>Found the form!</Box>
}

export default FormPage
