import React,  { ChangeEvent, useState } from "react"

import { Card, CardActions, CardContent, Grid, IconButton, TextField } from "@mui/material"
import DeleteIcon from '@mui/icons-material/Delete';

import { FormTextQuestion, Question } from "~/api/models"
import { QuestionList } from "~/contexts/QuestionList"
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
  // const [question, setQuestion] = useState((() => {
  //     const q = qList.questions[q_ind]
  //     return q ? q as FormTextQuestion : undefined
  // })())

  const [question, setQuestion] = useState(
    qList.questions[q_ind] as FormTextQuestion
  )

  const updateQuestion = (q_ind: number, q: Question) => {
    qOps.setQuestion(q_ind, q)
  }

  const delQuestion = () => {
    qOps.delQuestion(q_ind);
  }

  const myUpdateQ = (q: FormTextQuestion) => {
    console.log("Updating a question")
    setQuestion(q)
    qOps.setQuestion(q_ind - 1, q)
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

  return <>

    <CardContent>
    <Grid container>
      <Grid item xs={10}>
        <TextField required defaultValue={question.title}
          id="first-question-title" label="Question title"
          variant="standard" margin="normal"
          onChange={changeQuestionTitle}
          sx={{m: 0}}/>

        <TextField defaultValue={question.description}
          id="first-question-content" label="Question description"
          variant="filled" margin="normal"
          onChange={changeQuestionContent}
          sx={{p: 0}}/>

        <TextField required defaultValue={question.maxAnswerLength}
          id="first-question-length" label="Answer length"
          variant="filled" margin="normal" type='number'
          onChange={changeQuestionLength}
          sx={{p: 0}}/>
        </Grid>
      <Grid item xs={2}>
        <IconButton onClick={delQuestion}>
          <DeleteIcon></DeleteIcon>
        </IconButton>

        {/* <DeleteIcon></DeleteIcon> */}
      </Grid>
    </Grid>

    </CardContent>
  </>
}
