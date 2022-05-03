import { Box, Checkbox, Divider, FormControlLabel, Input, Typography } from "@mui/material"
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
    <Input multiline={true} style={{width: '100%'}} type="text" value={props.state.content}
      onChange={(e) => props.updater({...props.state,
          content: e.target.value || ""})}
    />
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
      />
    )}
  </Box>
}

const TickableOption = ({checked, content}: {checked: boolean, content: string}) =>
{
  return <Box>
    <FormControlLabel
      control={<Checkbox checked={checked} />} label={content}
      sx={{p: 0}}
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
        <Typography color="gray" variant="h5" sx={{mt: 3, mb: 1}}>
          #{i + 1}
        </Typography>
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
