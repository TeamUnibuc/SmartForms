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
  const [snackOpen, setSnackOpen] = useState(false)

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
      setSnackMsg("Answers submitted!  Redirecting ...")
      setSnackColor("success")
      // onOkSubmit()
      setTimeout(onOkSubmit, 2500)
    })
    .catch(er => {
      console.log(er)
      setSnackMsg("Error submitting answers :/")
      setSnackColor("error")
    })
    .finally(() => {
      console.log("Snack true")
      setSnackOpen(true)
    })
  }

  return <Box minWidth={'50%'}>
    <Button variant="contained" color="success" onClick={submitBtn}>
      Submit
    </Button>

    <Divider sx={{my: 2}} />

    <Typography variant="h4">
      {form.title}
    </Typography>
    <Typography>
      {form.description}
    </Typography>

    <Divider sx={{my: 2}} />

    <EditableAnswers
      answers={answers}
      questions={questions}
      updater={(a) => {setAnswers(a)}} />

    <DownSnackbar color={snackColor} msg={snackMsg}
      setSnackOpen={setSnackOpen} snackOpen={snackOpen}/>
  </Box>
}

export default EditAndSubmit
