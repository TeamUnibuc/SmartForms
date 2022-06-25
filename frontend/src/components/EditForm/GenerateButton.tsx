import React from 'react'

import Button from "@mui/material/Button";
import API from '~/api'
import { Question } from '~/api/models';
import { useQLContextState, useQLContextUpdater } from '~/contexts/QLContext';

interface BtnProps
{
  disabled?: boolean
}

export default function GenerateButton({disabled}: BtnProps): JSX.Element
{
  const {qList, title, description, needsToBeSignedInToSubmit, canBeFilledOnline} = useQLContextState()
  const {sOps} = useQLContextUpdater()

  const generatePdf = async (formData: Question[]) => {
    console.log(JSON.stringify(formData))
    const resp = await API.Form.FormPreview({
      authorEmail: "",
      formId: "",
      canBeFilledOnline: canBeFilledOnline,
      needsToBeSignedInToSubmit: needsToBeSignedInToSubmit,
      description: description,
      questions: formData,
      title: title
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

  return <Button disabled={disabled}
    variant="contained"
    onClick={() => generatePdf(getCuratedQuestions())}>

  Generate PDF

  </Button>
}
