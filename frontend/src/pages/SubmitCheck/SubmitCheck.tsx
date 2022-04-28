import React, { Dispatch, SetStateAction, SyntheticEvent, useEffect, useState } from 'react';

import { Button, Card, CardActionArea, CardActions, CardContent, FormControl, FormHelperText, Input, InputLabel, Typography } from '@mui/material';
import { InferenceResponse } from '~/api/inference/inference';
import API from '~/api'
import { FormAnswers } from '~/api/models';

interface SubmitCompProps {
  setInferenceDone: Dispatch<SetStateAction<boolean>>
  setAnswers: Dispatch<SetStateAction<InferenceResponse>>
}

const SubmitComp = (props: SubmitCompProps) =>
{
  const [files, setFiles] = useState<unknown>(undefined)
  const {setInferenceDone, setAnswers} = props

  const doUpload = async (files: FileList) => {
    const file = files[0]
    console.log(files)
    console.log("Querying the god damn inferencee")
    console.log(`I have file of  typ: ${file.type}`)
    let formData = new FormData();
    console.log("Appending")
    formData.append(`file.${file.type}`, file);
    console.log("Inference")
    const answers = await API.Inference.inference(formData)
    console.log(answers)
    setInferenceDone(true)
    setAnswers(answers)
  }

  const selectFile = (e: any) => {
    // console.log(e)
    const files = e.target.files as FileList
    // console.log(`Set file: ${e.}`)
    setFiles(files)
  }

  const sendButton = () => {
    doUpload(files as FileList)
  }

  return <>
    <FormControl>
      {/* <InputLabel htmlFor="my-file">Image/PDF/ZIP</InputLabel> */}
      <Input id="my-file" type="file" onChange={selectFile}/>
      <FormHelperText id="my-helper-text">We'll never share your email.</FormHelperText>
    </FormControl>
    <Button onClick={sendButton}>Send</Button>

    {/* <Button onClick={handleSpecialSubmit}>Go To Submit Page</Button> */}
  </>
}

const CheckComp = (props: {answers: FormAnswers[]}) =>
{
  const getLista = () => {
    return props.answers.map((ans, i) => {
      <Card key={i}>
        <CardActionArea>
          <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {ans.formId}
          </Typography>
          </CardContent>
        </CardActionArea>
        <CardActions>
          <Button>
            View / Edit
          </Button>
        </CardActions>
      </Card>
    })
  }

  return <>
    {getLista()}
  </>
}

const TryAgain = (props: {tryAgain(): void}) => {
  return <>
    <p>Din pacate am intampinat o eroare la parsarea fisierului/fisierelor</p>
    <Button onClick={props.tryAgain}>
      Try Again
    </Button>
  </>
}

export default function SubmitCheck(): JSX.Element
{
  const [inferenceDone, setInferenceDone] = useState(false)
  const [answers, setAnswers] = useState<InferenceResponse>([])

  if (!inferenceDone) {
    const submitProps = {
      setInferenceDone,
      setAnswers
    }
    return <SubmitComp {...submitProps}/>
  }

  if (typeof answers === 'string')
    return <TryAgain tryAgain={() => setInferenceDone(false)}/>

  return <CheckComp answers={answers}/>

}
