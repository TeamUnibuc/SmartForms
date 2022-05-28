import { useEffect, useState } from "react"
import { Link, useSearchParams } from "react-router-dom"

import { Box, Button, Typography } from "@mui/material"

import { FormDescription } from "~/api/models"
import SimpleMessage from "~/components/SimpleMessage"
import EditAndSubmit from "./EditAndSubmit"
import API from "~/api"

const FastSubmit = () =>
{
  const [searchParams, _setSearchParams] = useSearchParams()
  const [loading, setLoading] = useState(true)
  const [formData, setFormData] = useState<undefined | FormDescription>()
  const [formSent, setFormSent] = useState(false)

  const formId = searchParams.get("formId") || ""

  useEffect(() => {
    API.Form.Description(formId)
    .then(r => {
      setFormData(r)
    })
    .catch(er => {
      console.log(er)
    })
    .finally(() => {
      setLoading(false)
    })
  }, [])

  if (formSent) {
    return <Box>
      <Typography>
        You are done!
      </Typography>
      <Button
        variant="contained"
        component={Link}
        style={{backgroundColor: '#568e00'}}
        // onClick={handleCloseNavMenu}
        sx={{ my: 2, color: 'white' }}
        to={'/list'}
      >
        Go to All Forms
      </Button>
    </Box>
  }

  return <Box>
      {loading ?
          <SimpleMessage color="info" msg="Loading..." />
      :
        formData ?
          <EditAndSubmit form={formData} onOkSubmit={() => setFormSent(true)}/>
        :
          <SimpleMessage color="error" msg="Invalid Form :/" />
      }
  </Box>
}

export default FastSubmit
