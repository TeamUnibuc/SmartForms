import { useState } from "react"
import { Alert, AlertColor, Button, IconButton, Snackbar } from "@mui/material"

import API from "~/api"
import { Question } from "~/api/models"
import { useQLContextState } from "~/contexts/CoolContext"
import DownSnackbar from "../DownSnackbar"

interface FormBtnProps
{
  disabled?: boolean
}

const CreateFormButton = ({disabled}: FormBtnProps) =>
{
  const {qList, canBeFilledOnline, needsToBeSignedInToSubmit, description, title} = useQLContextState()
  const [snackOpen, setSnackOpen] = useState(false)
  const [snackState, setSnackState] = useState<{msg: string, color: AlertColor}>({msg: "", color: "info"})

  const getCuratedQuestions = (): Question[] => {
    const notundef = <T,>(x: T | undefined): x is T => {
      return x !== undefined
    };
    return qList.questions.filter(notundef)
  }

  const onCreateClick = () =>
  {
    API.Form.FormCreate({
      authorEmail: "",
      formId: "",
      canBeFilledOnline: canBeFilledOnline,
      description: description,
      needsToBeSignedInToSubmit: needsToBeSignedInToSubmit,
      title: title,
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

  return <>
  <Button sx={{mt: 2}} disabled={disabled}
    variant="contained"
    color="success"
    onClick={onCreateClick}>

  Create Form

  </Button>

  <DownSnackbar
    snackOpen={snackOpen}
    setSnackOpen={setSnackOpen}
    color={snackState.color}
    msg={snackState.msg}
  />
  </>
}

export default CreateFormButton
