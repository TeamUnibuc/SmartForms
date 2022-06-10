import React,  { ChangeEvent, useEffect, useState } from "react"

import { Box, Card, CardActions, CardContent, Checkbox, FormControlLabel, Grid, IconButton, TextField, Typography } from "@mui/material"
import DeleteIcon from '@mui/icons-material/Delete';

import { FormTextQuestion } from "~/api/models"
import { useQLContextState, useQLContextUpdater } from "~/contexts/CoolContext"

interface ComponentProps
{
  q_ind: number
}

export default function TQText(props: ComponentProps): JSX.Element
{
  const q_ind = props.q_ind;
  const {qList} = useQLContextState()
  const {qOps} = useQLContextUpdater()

  const [cLower, setCLower] = useState(false)
  const [cUpper, setCUpper] = useState(false)
  const [cDigits, setDigits] = useState(false)
  const [cOther, setCOther] = useState(false)

  const [question, setQuestion] = useState(
    qList.questions[q_ind] as FormTextQuestion
  )

  const delQuestion = () => {
    qOps.delQuestion(q_ind);
  }

  const myUpdateQ = (q: FormTextQuestion) => {
    console.log("Updating a question")
    setQuestion(q)
    qOps.setQuestion(q_ind, q)
  }

  const changeQuestionTitle = (e: ChangeEvent<HTMLInputElement>)  => {
    const newq = {...question as FormTextQuestion, title: e.target.value}
    myUpdateQ(newq)
  }

  const changeQuestionContent = (e: ChangeEvent<HTMLInputElement>)  => {
    const newq = {...question, description: e.target.value}
    myUpdateQ(newq)
  }

  const changeQuestionLength = (e: ChangeEvent<HTMLInputElement>)  => {
    const newq = {...question, maxAnswerLength: Number(e.target.value)}
    myUpdateQ(newq)
  }

  useEffect(() => {
    const newq: FormTextQuestion = {
      ...question,
      allowedCharacters:
        (cLower ? 'abcdefghijklmnopqrstuvwxyz' : '') +
        (cUpper ? 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' : '') + 
        (cDigits ? '0123456789' : '') + 
        (cOther ? '-_*+.' : '') 
    }

    myUpdateQ(newq)
  }, [cLower, cUpper, cOther, cDigits])

  return <>
    <CardContent>
    <Grid container>
      <Grid item xs={10}>
        <TextField required fullWidth
          style={{width: '95%'}}
          defaultValue={question.title}
          label="Question title"
          variant="standard" margin="normal"
          onChange={changeQuestionTitle}
          sx={{m: 0}}/>

        <TextField defaultValue={question.description}
          label="Question description"
          variant="filled" margin="normal"
          onChange={changeQuestionContent}
          sx={{p: 0}}/>

        <TextField required defaultValue={question.maxAnswerLength}
          label="Answer length"
          variant="filled" margin="normal" type='number'
          onChange={changeQuestionLength}
          sx={{p: 0}}/>

        <Typography sx={{mt: 1.5}}>
          Check allowed characters
        </Typography>
        <Box display='flex' flexWrap={'wrap'}>
          <TickableOption checked={cLower} content={'a-z'} updater={(s) => setCLower(s)} />
          <TickableOption checked={cUpper} content={'A-Z'} updater={(s) => setCUpper(s)} />
          <TickableOption checked={cDigits} content={'0-9'} updater={(s) => setDigits(s)} />
          <TickableOption checked={cOther} content={'other'} updater={(s) => setCOther(s)} />
        </Box>
        </Grid>
      <Grid item xs={2}>
        <IconButton onClick={delQuestion}>
          <DeleteIcon />
        </IconButton>
      </Grid>
    </Grid>

    </CardContent>
  </>
}

const TickableOption = ({checked, content, updater}: {checked: boolean, content: string, updater(s: boolean): void}) =>
{
  return <Box style={{minWidth: '50%'}}>
    <FormControlLabel
      control={<Checkbox checked={checked} />} label={content}
      sx={{p: 0}} onChange={(e, e_checked: boolean) => updater(e_checked)}
    />
  </Box>
}
