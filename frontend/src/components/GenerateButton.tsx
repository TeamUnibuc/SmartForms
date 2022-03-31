import React, { useContext } from 'react'

import Button from "@mui/material/Button";
import { QuestionList } from '~/contexts/QuestionList';
import { FormPreview } from '~/api/form/preview';
import { Question } from '~/api/models';

export default function GenerateButton(): JSX.Element
{
  const qlContext = useContext(QuestionList)
  const {setPdfString} = qlContext.pdfData

  const generatePdf = async (formData: Question[]) => {
    console.log(JSON.stringify(formData))
    const resp = await FormPreview({
      canBeFilledOnline: true,
      needsToBeSignedInToSubmit: true,
      description: "useless description",
      questions: formData,
      title: "First PDF"}
    )
    console.log("Setting pdfbase64 new data")
    setPdfString(resp.formPdfBase64)
  }

  console.log("R - Button ")

  return <Button
    variant="contained"
    onClick={() => generatePdf(qlContext.qList.questions)}>

  Generate PDF

  </Button>
}
