import { StatusPanelComponent } from "@ag-grid-community/core/dist/cjs/es5/components/framework/componentTypes"
import { Box, Checkbox, Divider, FormControlLabel, Input, TextField, Typography } from "@mui/material"
import { useState } from "react"
import { FormMultipleChoiceQuestion, FormTextQuestion, MultipleChoiceAnswer, Question, SingleQAnswer, TextAnswer } from "~/api/models"

interface EAProps
{
  answers: SingleQAnswer[],
  questions: Question[],
  updater(answers: SingleQAnswer[]): void
}

const EditTextQ = (props: {
  question: FormTextQuestion,
  state: TextAnswer,
  updater(a: TextAnswer): void
}) =>
{
  

  return <Box>
    <TextField defaultValue={props.state.content}
      id="form-desc"
      label="Answer"
      variant="filled"
      margin="normal"
      onChange={(e) => props.updater({...props.state,
        content: e.target.value || ""})}
      sx={{m: 0, p: 0}}
      style={{width: "100%"}}
    />

    

    {/* <Input
        multiline={true}
        style={{width: '100%'}}
        type="text"
        value={props.state.content}
        onChange={(e) => props.updater({...props.state,
          content: e.target.value || ""})}
    /> */}
  </Box>
}

const EditMChoiceQ = (props: {
  question: FormMultipleChoiceQuestion,
  state: MultipleChoiceAnswer,
  updater(a: MultipleChoiceAnswer): void
}) =>
{
  return <Box>
    {props.question.choices.map((ch, idx) =>
      <TickableOption
        checked={props.state.content[idx] !== ' '}
        content={ch}
        key={idx}
        updater={(state: boolean) => {
          const replacer = (s: string, i: number, ch: string) => {
            return s.substring(0, i) + ch + s.substring(i + 1)
          }
          let newContent = replacer(props.state.content, idx, state ? 'X' : ' ')
          props.updater({...props.state, content: newContent})
        }}
      />
    )}
  </Box>
}

const TickableOption = ({checked, content, updater}: {checked: boolean, content: string, updater(s: boolean): void}) =>
{
  return <Box>
    <FormControlLabel
      control={<Checkbox checked={checked} />} label={content}
      sx={{p: 0}} onChange={(e, e_checked: boolean) => updater(e_checked)}
    />
  </Box>
}

const EditableAnswers = ({answers, questions, updater}: EAProps) =>
{
  const updateNthAnswer = (idx: number) =>
  {
    const update = (ans: SingleQAnswer) => {
      const newAnswers = [...answers]
      newAnswers[idx] = ans
      updater(newAnswers)
    }

    return update
 }

  return <>
    {answers.map((ans, i) => {
      const q = questions[i]
      return <Box key={i}>
        <Typography color="gray" variant="h5" sx={{mt: 2}}>
          #{i + 1}
        </Typography>
        <Divider color="#000" sx={{mb: 1}} style={{borderWidth: '2px'}}/>

        <Typography variant="h6">
          {q.title}
        </Typography>
        <Typography variant="h6" color="gray" fontSize="1rem">
          {q.description}
        </Typography>

        <Divider />

        {(q as FormTextQuestion).maxAnswerLength !== undefined ?
        <EditTextQ
          question={q as FormTextQuestion}
          state={ans as TextAnswer}
          updater={updateNthAnswer(i)}
        />
      :
        <EditMChoiceQ
          question={q as FormMultipleChoiceQuestion}
          state={ans as MultipleChoiceAnswer}
          updater={updateNthAnswer(i)}
        />
      }

      </Box>
    })}
  </>
}

export default EditableAnswers
