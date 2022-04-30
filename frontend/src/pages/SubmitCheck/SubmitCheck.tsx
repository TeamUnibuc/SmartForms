import React, { Dispatch, SetStateAction, SyntheticEvent, useEffect, useState } from 'react';

import { Box, Button, Card, CardActionArea, CardActions, CardContent, Container, Divider, FormControl, FormGroup, FormHelperText, Input, InputLabel, TextField, Typography } from '@mui/material';
import { InferenceResponse } from '~/api/inference/infer';
import API from '~/api'
import { FormAnswers, FormDescription } from '~/api/models';

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
    {/* Old options */}
    {/* <Box>
      <form action="/api/inference/infer" encType="multipart/form-data" method="post">
      <input name="fileUploads" type="file" multiple />
      <input type="submit" />
      </form>
    </Box>
  */}

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

  <FormControl variant="filled">
    <Input id="my-file" type="file" name='fileUploads'
      onChange={selectFile}
      inputProps={{
        multiple: true
      }}/>

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

const FormCardCheck = (props: {answer: FormAnswers, idx: number}) =>
{
  const [formInfo, setFormInfo] = useState<undefined | FormDescription>()
  const [cardTitle, setCardTitle] = useState(props.answer.formId)

  useEffect(() => {
    const sleep = (time: number) => {
      return new Promise((resolve) => setTimeout(resolve, time));
    }

    const myf = async () => {
      const data = await API.Form.Description(props.answer.formId)
      await sleep(900)
      setFormInfo(data)
      setCardTitle(data.title)
    }

    myf()
  }, [])

  return <Card style={{minWidth: "15em"}}>
    <CardActionArea>
      <CardContent>
      <Typography gutterBottom variant="h5" component="div">
        <span style={{color: "gray"}}>
          #{props.idx + 1 + " "}
        </span>
        {cardTitle}
      </Typography>
      <Typography>
        <span style={{color: "gray"}}>Answers: </span>
        {props.answer.answers.length}
      </Typography>
      </CardContent>
    </CardActionArea>
    <CardActions>
      <Box textAlign='center' width='100%'>
        <Button variant="outlined">
          View / Edit
        </Button>
      </Box>
    </CardActions>
  </Card>
}

const CheckComp = (props: {answers: FormAnswers[]}) =>
{
  console.log(props.answers)

  const getLista = () => {
    return props.answers.map((ans, i) => {
      return <FormCardCheck answer={ans} key={i} idx={i}/>
    })
  }

  return <Box>
    <Container>
      {getLista()}
    </Container>
    <Divider sx={{m: 1}} orientation="horizontal"/>
    <Button variant="contained" color="success">
      Submit Answers
    </Button>
  </Box>
}

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

  return <CheckComp answers={answers}/>

}
