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
        component={Link}
        // onClick={handleCloseNavMenu}
        sx={{ my: 2, color: 'white', display: 'block' }}
        to={'/list'}
      >
        Go to All Forms
      </Button>
    </Box>
  }

  return <Box id="fast-submit" display="flex" justifyContent={'center'}>
      {loading ?
        <Box  width='min-content'>
          <SimpleMessage color="info" msg="Loading..." />
        </Box>
      :
        formData ?
          <EditAndSubmit form={formData} onOkSubmit={() => setFormSent(true)}/>
        :
          <SimpleMessage color="error" msg="Invalid Form :/" />
      }
  </Box>
}

export default FastSubmit
