import React, { Dispatch, SetStateAction, SyntheticEvent, useEffect, useState } from 'react';

import { Box, Button, Card, CardActionArea, CardActions, CardContent, Divider, FormControl, FormGroup, FormHelperText, Input, InputLabel, TextField, Typography } from '@mui/material';
import { InferenceResponse } from '~/api/inference/infer';
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
    console.log("Querying the god damn inferencee")
    let formData = new FormData();
    for (const file of files) {
      formData.append(`fileUploads`, file, file.name)
    }
    const answers = await API.Inference.Infer(formData)
    setInferenceDone(true)
    setAnswers(answers)
  }

  const selectFile = (e: any) => {
    const files = e.target.files as FileList
    setFiles(files)
  }

  const sendButton = () => {
    doUpload(files as FileList)
  }

  return <>
  <Box>
    <form action="/api/inference/infer" encType="multipart/form-data" method="post">
    <input name="fileUploads" type="file" multiple />
    <input type="submit" />
    </form>
  </Box>



    <FormControl variant="filled">
      <Input id="my-file" type="file" name='fileUploads'
        onChange={selectFile}
        inputProps={{
          multiple: true
        }}/>
      {/* <form action="/api/inference/infer" encType="multipart/form-data" method="post">
        <TextField
          id="outlined-basic"
          label="Outlined"
          variant="outlined"
          type="file"
          inputProps={{
            multiple: true,
            type: "file",
            name: "fileUploads"
          }}
        />

        <Input type="submit"/> */}


      {/* </form> */}

      <FormHelperText id="my-helper-text">
          Placeholder text
        </FormHelperText>

    </FormControl>
    <Divider />
    <Button onClick={sendButton} variant="contained">
      Send
    </Button>
  </>
}

const CheckComp = (props: {answers: FormAnswers[]}) =>
{
  console.log(props.answers)
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

  return <CheckComp answers={answers}/>

}
