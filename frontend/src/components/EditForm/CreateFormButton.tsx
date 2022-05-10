import { useState } from "react"
import { Alert, AlertColor, Button, IconButton, Snackbar } from "@mui/material"

import API from "~/api"
import { Question } from "~/api/models"
import { useQLContextState } from "~/contexts/CoolContext"

const CreateFormButton = () =>
{
  const {qList} = useQLContextState()
  const [snackOpen, setSnackOpen] = useState(false)
  const [snackState, setSnackState] = useState({msg: "", color: "info"})

  const getCuratedQuestions = (): Question[] => {
    const notundef = <T,>(x: T | undefined): x is T => {
      return x !== undefined
    };
    return qList.questions.filter(notundef)
  }

  const onCreateClick = () =>
  {
    API.Form.FormCreate({
      canBeFilledOnline: true,
      description: "Descriere :)",
      formId: "",
      needsToBeSignedInToSubmit: false,
      title: "Titlu Form",
      questions: getCuratedQuestions()
    })
    .then(r => {
      console.log(r)
      setSnackState({
        color: "success",
        msg: `Form created successfully with ID: ${r.formId}`
      })
      setSnackOpen(true)
    })
    .catch(r => {
      setSnackState({
        color: "error",
        msg: `Error occured :/`
      })
      console.log(r)
    })
    .finally(() => {
      setSnackOpen(true)
    })
  }

  const handleSnackClose = (event: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackOpen(false);
  };

  return <>
  <Button sx={{mt: 2}}
    variant="contained"
    color="success"
    onClick={onCreateClick}>

  Create Form

  </Button>
  <Snackbar
    open={snackOpen}
    autoHideDuration={6000}
    onClose={handleSnackClose}
  >
    <Alert
      onClose={handleSnackClose}
      severity={snackState.color as AlertColor}
      sx={{ width: '100%' }}
    >
      {snackState.msg}
    </Alert>
  </Snackbar>
  </>
}

export default CreateFormButton
