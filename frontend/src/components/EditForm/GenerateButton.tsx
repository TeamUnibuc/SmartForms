import React from 'react'

import Button from "@mui/material/Button";
import API from '~/api'
import { Question } from '~/api/models';
import { useQLContextState, useQLContextUpdater } from '~/contexts/CoolContext';

export default function GenerateButton(): JSX.Element
{
  const {qList} = useQLContextState()
  const {sOps} = useQLContextUpdater()

  const generatePdf = async (formData: Question[]) => {
    console.log(JSON.stringify(formData))
    const resp = await API.Form.FormPreview({
      authorEmail: "",
      formId: "",
      canBeFilledOnline: true,
      needsToBeSignedInToSubmit: true,
      description: "useless description",
      questions: formData,
      title: "First PDF"
    })
    sOps.setPdfString(resp.formPdfBase64)
  }

  console.log("R - Button ")

  const getCuratedQuestions = (): Question[] => {
    const notundef = <T,>(x: T | undefined): x is T => {
      return x !== undefined
    };
    return qList.questions.filter(notundef)
  }

  return <Button
    variant="contained"
    onClick={() => generatePdf(getCuratedQuestions())}>

  Generate PDF

  </Button>
}
