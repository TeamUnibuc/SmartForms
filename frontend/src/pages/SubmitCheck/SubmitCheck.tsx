import React, { Dispatch, SetStateAction, SyntheticEvent, useEffect, useState } from 'react';

import { Box, Button, Card, CardActionArea, CardActions, CardContent, Container, Divider, FormControl, FormGroup, FormHelperText, Input, InputLabel, Modal, TextField, Typography } from '@mui/material';
import { InferenceResponse } from '~/api/inference/infer';
import API from '~/api'
import { FormAnswers, FormDescription } from '~/api/models';

type ModalDataType = undefined | {
  fAns: FormAnswers,
  fDesc: FormDescription
}

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

const FormCardCheck = (props: {
    answer: FormAnswers,
    idx: number,
    openModal(): void,
    setModalData(d: ModalDataType): void}) =>
{
  const [formInfo, setFormInfo] = useState<undefined | FormDescription>()
  const [cardTitle, setCardTitle] = useState(props.answer.formId)

  useEffect(() => {
    const sleep = (time: number) => {
      return new Promise((resolve) => setTimeout(resolve, time));
    }

    const getInfo = async () => {
      const data = await API.Form.Description(props.answer.formId)
      await sleep(600)
      setFormInfo(data)
      setCardTitle(data.title)
    }

    getInfo()
  }, [])

  const viewEditClick = () => {
    if (formInfo) {
      props.setModalData({
        fAns: props.answer,
        fDesc: formInfo
      })
      props.openModal()
    }
  }

  return <Card style={{minWidth: "15em"}} sx={{m: 1}}>
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
        <Button variant="outlined" onClick={viewEditClick}>
          View / Edit
        </Button>
      </Box>
    </CardActions>
  </Card>
}

const CheckComp = (props: {answers: FormAnswers[]}) =>
{
  const [open, setOpen] = useState(false);
  const [modalData, setModalData] = useState<ModalDataType>(undefined)
  const setModalOpen = () => setOpen(true);
  const setModalClose = () => setOpen(false);

  const tryOpenModal = () => {
    if (open)
      return
    setModalOpen()
  }

  const style = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

  const getLista = () => {
    return props.answers.map((ans, i) => {
      return <FormCardCheck
        answer={ans}
        openModal={tryOpenModal} setModalData={d => setModalData(d)}
        key={i} idx={i}/>
    })
  }

  return <Box>
    <Modal
      open={open}
      onClose={setModalClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
      {modalData === undefined ?
        <Typography>Weird, this shouldnt happend</Typography>
       : <>
        <Typography id="modal-modal-title" variant="h6" component="h2">
          {modalData.fDesc.title}
        </Typography>
        <Typography id="modal-modal-description" sx={{ mt: 2 }}>
          {modalData.fAns.formId}
        </Typography>
       </>
      }

      </Box>
    </Modal>

    <Box sx={{display: 'flex'}}>
      {getLista()}
    </Box>
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
