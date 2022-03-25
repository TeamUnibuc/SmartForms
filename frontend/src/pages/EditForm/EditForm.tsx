import React, { useState } from 'react'

import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import PdfDisplay from './PdfDisplay';

import {FormPreview} from '../../api/form/preview'

export default function EditForm(): JSX.Element
{
  const [formData, setFormData] = useState([]);
  const [pdfData, setPdf] = useState('')

  const generatePdf = async () => {
    const resp = await FormPreview({
      canBeFilledOnline: true,
      needsToBeSignedInToSubmit: true,
      description: "useless description",
      questions: [
        {title: "qq11",
        description: "mare descriere",
        maxAnswerLength: 12}
      ],
      title: "First PDF"}
    )
    console.log("Setting pdfbase64 new data")
    setPdf(resp.formPdfBase64)
  }

  return <>
    <Grid container columnSpacing={1}>
      <Grid item xs={4}>
        <p>Ceva text</p>
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
