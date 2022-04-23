import React, { ChangeEvent, useState } from "react"

import ClearIcon from '@mui/icons-material/Clear';
import { FormMultipleChoiceQuestion } from "~/api/models";
import { useQLContextState, useQLContextUpdater } from "~/contexts/CoolContext";
import { CardContent, Grid, IconButton, TextField } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

interface ComponentProps
{
  q_ind: number
}

export default function TQMultipleChoice(props: ComponentProps): JSX.Element
{
  const q_ind = props.q_ind;
  const {qList} = useQLContextState()
  const {qOps} = useQLContextUpdater()

  const [question, setQuestion] = useState(
    qList.questions[q_ind] as FormMultipleChoiceQuestion
  )

  const delQuestion = () => {
    qOps.delQuestion(q_ind);
  }

  const myUpdateQ = (q: FormMultipleChoiceQuestion) => {
    console.log("Updating a question")
    setQuestion(q)
    qOps.setQuestion(q_ind, q)
  }

  const changeQuestionTitle = (e: ChangeEvent<HTMLInputElement>)  => {
    const newq = {...question, title: e.target.value}
    myUpdateQ(newq)
  }

  const changeChoice = (index: number) => {
    const updater = (e: ChangeEvent<HTMLInputElement>) => {
      question.choices[index] = e.target.value
      myUpdateQ(question)
    }

    return updater
  }

  const QuestionList = () => {
    const lista = question.choices.map((choice, i) => {
      return (
        <TextField defaultValue={choice}
          id="first-question-content" label="Question description"
          variant="filled" margin="normal"
          onChange={changeChoice(i)}
          sx={{p: 0}}
      />)
    })

    return <>
      {lista}
    </>
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

        {QuestionList()}
        </Grid>
      <Grid item xs={2}>
        <IconButton onClick={delQuestion}>
          <DeleteIcon></DeleteIcon>
        </IconButton>
      </Grid>
    </Grid>
    </CardContent>
  </>
}
