import { useState } from "react"
import { Alert, AlertColor, Button, IconButton, Snackbar } from "@mui/material"

import API from "~/api"
import { Question } from "~/api/models"
import { useQLContextState } from "~/contexts/QLContext"
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
    .then(async r => {
      console.log(r)
      setSnackState({
        color: "success",
        msg: `Form created successfully with ID: ${r.formId}   Redirecting ...`
      })
      setSnackOpen(true)

      const sleep = (time: number) => {
        return new Promise((resolve) => setTimeout(resolve, time));
      }

      await sleep(2000)
      window.location.href = `/form?formId=${r.formId}`
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
