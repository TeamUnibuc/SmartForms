import { useEffect, useState } from "react"
import { Link, useSearchParams, useNavigate } from "react-router-dom"

import { Box, Button, Typography } from "@mui/material"

import { FormDescription } from "~/api/models"
import SimpleMessage from "~/components/SimpleMessage"
import EditAndSubmit from "./EditAndSubmit"
import API from "~/api"

const FastSubmit = () =>
{
  const navigate = useNavigate()
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

  const onOkSubmit = async () => {
    // setFormSent(true)

    const sleep = (time: number) => {
      return new Promise((resolve) => setTimeout(resolve, time));
    }

    await sleep(2000)
    // window.location.href = `/form?formId=${formId}`
    navigate(`/form?formId=${formId}`)
  }

  if (formSent) {
    return <Box>
      <Typography>
        You are done!
      </Typography>
      <Button
        variant="contained"
        component={Link}
        style={{backgroundColor: '#568e00'}}
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
          <EditAndSubmit form={formData} onOkSubmit={onOkSubmit}/>
        :
          <SimpleMessage color="error" msg="Invalid Form :/" />
      }
  </Box>
}

export default FastSubmit
