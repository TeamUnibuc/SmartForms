import { AlertColor, Box, Button, Divider, Typography } from "@mui/material"
import { useState } from "react"
import API from "~/api"
import { FormDescription, FormMultipleChoiceQuestion } from "~/api/models"

import { SingleQAnswer } from "~/api/models"
import DownSnackbar from "~/components/DownSnackbar"
import EditableAnswers from "~/components/EditableAnswers"

interface EASProps
{
  form: FormDescription
  onOkSubmit(): void
}

const EditAndSubmit = ({form, onOkSubmit}: EASProps) =>
{
  const {questions} = form
  const [snackMsg, setSnackMsg] = useState("")
  const [snackColor, setSnackColor] = useState<AlertColor>("info")
  const [showSnack, setShowSnack] = useState(false)

  const transformContent = (idx: number) => {
    const qmc = questions[idx] as FormMultipleChoiceQuestion
    if (qmc.choices !== undefined)
      return " ".repeat(qmc.choices.length)
    return ""
  }

  const [answers, setAnswers] = useState<SingleQAnswer[]>(
    questions.map((_q, idx) => ({content: transformContent(idx)})))

  const submitBtn = () =>
  {
    API.Entry.Create({answers: answers, formId: form.formId})
    .then(r => {
      setSnackMsg("Answers submitted!")
      setSnackColor("success")
    })
    .catch(er => {
      console.log(er)
      setSnackMsg("Error submitting answers :/")
      setSnackColor("error")
    })
    .finally(() => {
      setShowSnack(true)
    })
  }

  return <Box minWidth={'50%'}>
    <Button variant="contained" color="success" onClick={submitBtn}>
      Submit
    </Button>

    <Divider sx={{my: 2}} />

    <EditableAnswers
      answers={answers}
      questions={questions}
      updater={(a) => {setAnswers(a)}} />

    <DownSnackbar color={snackColor} msg={snackMsg} initShow={showSnack}/>


  </Box>
}

export default EditAndSubmit
