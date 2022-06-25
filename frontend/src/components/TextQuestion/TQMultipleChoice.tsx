import React, { ChangeEvent, useState } from "react"

import ClearIcon from '@mui/icons-material/Clear';
import AddIcon from '@mui/icons-material/Add';
import { FormMultipleChoiceQuestion } from "~/api/models";
import { useQLContextState, useQLContextUpdater } from "~/contexts/QLContext";
import { Box, CardContent, Grid, IconButton, TextField } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

interface ComponentProps
{
  q_ind: number
}

export default function TQMultipleChoice(props: ComponentProps): JSX.Element
{
  console.log("Render TQMultiple")

  const q_ind = props.q_ind;
  const {qList} = useQLContextState()
  const {qOps} = useQLContextUpdater()

  const [question, setQuestion] = useState(
    qList.questions[q_ind] as FormMultipleChoiceQuestion
  )

  console.log("State has questions: ")
  console.log(question)

  const delQuestion = () => {
    qOps.delQuestion(q_ind);
  }

  const myUpdateQ = (q: FormMultipleChoiceQuestion) => {
    console.log("Updating a question")
    const newestuff = {...q, title: q.title}
    setQuestion(newestuff)
    qOps.setQuestion(q_ind, q)
  }

  const changeQuestionTitle = (e: ChangeEvent<HTMLInputElement>)  => {
    const newq = {...question, title: e.target.value}
    myUpdateQ(newq)
  }

  const changeQuestionDescription = (e: ChangeEvent<HTMLInputElement>)  => {
    const newq = {...question, description: e.target.value}
    myUpdateQ(newq)
  }

  const changeChoice = (index: number) => {
    const updater = (e: ChangeEvent<HTMLInputElement>) => {
      question.choices[index] = e.target.value
      const wtf = {...question, title: question.title}
      myUpdateQ(wtf)
    }

    return updater
  }

  const deleteChoice = (index: number) => {
    const updater = () => {
      console.log("Before:")
      console.log(question.choices)
      for (let i = index; i + 1 < question.choices.length; ++i){
        question.choices[i] = question.choices[i + 1]
        console.log(i)
      }
      question.choices.pop()
      console.log("after")
      console.log(question.choices)
      myUpdateQ(question)
    }

    return updater
  }

  const QuestionList = () => {
    const lista = question.choices.map((choice, i) => {
      console.log(`Reredering option ${i} with: ${choice}`)
      return (<Box key={q_ind + "-" + i}>
        <TextField value={choice}
          label="Question description"
          variant="filled" margin="normal"
          onChange={changeChoice(i)}
          sx={{p: 0, marginTop: 0.5}}
        />
        <IconButton onClick={deleteChoice(i)}
          style={{height: "100%", marginTop: "0.5em"}}>
          <ClearIcon />
      </IconButton>
    </Box>)
    })

    return <>
      {lista}
    </>
  }

  const DeleteIconsList = () => {
    const lista = question.choices.map((choice, i) => {
      return (
        <IconButton onClick={deleteChoice(i)}
         sx={{height: "73px"}} key={q_ind + "--" + i}>
          <ClearIcon />
        </IconButton>
      )
    })

    return <>{lista}</>
  }

  const addChoice = () => {
    const newindex = question.choices.length
    question.choices[newindex] = `Option ${newindex + 1}`
    myUpdateQ(question)
  }

  return <>
    <CardContent>
    <Grid container>
      <Grid item xs={10}>
        <TextField required fullWidth
          defaultValue={question.title}
          style={{maxWidth: '95%'}}
          label="Question title"
          variant="standard" margin="normal"
          onChange={changeQuestionTitle}
          sx={{m: 0}}/>


      </Grid>
      <Grid item xs={2}>
        <IconButton onClick={delQuestion}
         sx={{mb: 2}}>
          <DeleteIcon />
        </IconButton>

      </Grid>

      <Grid item xs={12}>
        <TextField fullWidth
            defaultValue={question.description}
            style={{maxWidth: '95%'}}
            label="Question description"
            variant="standard" margin="normal"
            onChange={changeQuestionDescription}
            sx={{mb: 1}}/>
      </Grid>

      <Grid item xs={12}>
        {QuestionList()}
        {/* {DeleteIconsList()} */}

      </Grid>

      <Grid item>
        <IconButton onClick={addChoice}>
          <AddIcon />
        </IconButton>
      </Grid>
    </Grid>
    </CardContent>
  </>
}
