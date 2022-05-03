import React, { useState } from 'react';

import { Button } from '@mui/material';
import { InferenceResponse } from '~/api/inference/infer';
import SubmitComp from './SubmitComp';
import CheckComp from './CheckComp';

const TryAgain = (props: {tryAgain(): void}) => {
  return <>
    <p>Din pacate am intampinat o eroare la parsarea fisierului/fisierelor</p>
    <Button onClick={props.tryAgain} variant="outlined">
      Try Again
    </Button>
  </>
}

export default function SubmitCheck(): JSX.Element
{
  const [inferenceDone, setInferenceDone] = useState(false)
  const [answers, setAnswers] = useState<InferenceResponse>([])

  console.log("Rendering SubmitCheck")

  if (!inferenceDone) {
    const submitProps = {
      setInferenceDone,
      setAnswers
    }
    return <SubmitComp {...submitProps}/>
  }

  if (typeof answers === 'string')
    return <TryAgain tryAgain={() => setInferenceDone(false)}/>

  return <CheckComp answers={answers} setAnswers={(x) => setAnswers(x)}/>
}
