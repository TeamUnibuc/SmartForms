import React, { ChangeEvent, SyntheticEvent, useState } from 'react'

import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import PdfDisplay from './PdfDisplay';

import { FormPreview } from '~/api/form/preview'
import { FormTextQuestion } from '~/api/models';
import TextField from '@mui/material/TextField';

export default function EditForm(): JSX.Element
{
  const [formData, setFormData] = useState([])
  const [pdfData, setPdf] = useState('')

  const [question, setQuestion] = useState<FormTextQuestion>({
    description: "",
    maxAnswerLength: 5,
    title: "Question title"
  })

  const changeQuestionTitle = (e: ChangeEvent<HTMLInputElement>)  => {
    console.log("title changed")
    setQuestion({...question, title: e.target.value || ""})
  }

  const changeQuestionContent = (e: ChangeEvent<HTMLInputElement>)  => {
    setQuestion({...question, description: e.target.value || ""})
  }

  const changeQuestionLength = (e: ChangeEvent<HTMLInputElement>)  => {
    setQuestion({...question, maxAnswerLength: Number(e.target.value) || 5})
  }

  const generatePdf = async () => {
    console.log(question)
    const resp = await FormPreview({
      canBeFilledOnline: true,
      needsToBeSignedInToSubmit: true,
      description: "useless description",
      questions: [
        question
      ],
      title: "First PDF"}
    )
    console.log("Setting pdfbase64 new data")
    setPdf(resp.formPdfBase64)
  }

  return <>
    <Grid container columnSpacing={1}>
      <Grid item xs={4}>
        <TextField required
          id="first-question-title" label="Question title"
          variant="filled" margin="normal"
          onChange={changeQuestionTitle}/>
        <TextField
          id="first-question-content" label="Question description"
          variant="filled" margin="normal"
          onChange={changeQuestionContent}/>
        <TextField required
          id="first-question-length" label="Answer length"
          variant="filled" margin="normal" type='number'
          onChange={changeQuestionLength}/>
      </Grid>

      <Grid item xs={2}>
        <Button variant="contained" onClick={generatePdf}>Generate PDF</Button>
      </Grid>

      <Grid item xs={6}>
        <PdfDisplay pdfb64={pdfData}/>
      </Grid>
    </Grid>
  </>
}
