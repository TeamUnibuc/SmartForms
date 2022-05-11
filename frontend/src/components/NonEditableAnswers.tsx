import { Box, Checkbox, Divider, FormControlLabel, Input, Typography } from "@mui/material"
import { FormMultipleChoiceQuestion, FormTextQuestion, MultipleChoiceAnswer, Question, SingleQAnswer, TextAnswer } from "~/api/models"

interface EAProps
{
  questions: Question[]
}

const MChoiceQ = (props: {
  question: FormMultipleChoiceQuestion
}) =>
{
  return <Box>
    {props.question.choices.map((ch, idx) =>
      <TickableOption
        checked={false}
        content={ch}
        key={idx}
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

const NonEditableAnswers = ({questions}: EAProps) =>
{
  return <>
    {questions.map((q, i) => {
      return <Box key={i}>
        <Typography color="#a1c9c5" variant="h5" sx={{mt: 2}} style={{fontWeight: 700}}>
          #{i + 1}
        </Typography>
        <Divider color="#000" sx={{mb: 1}} style={{borderWidth: '2px'}}/>

        <Typography variant="h6">
          {q.title}
        </Typography>
        <Typography variant="h6" color="gray" fontSize="1rem">
          {q.description}
        </Typography>

        {(q as FormTextQuestion).maxAnswerLength !== undefined ?
        <>
          {/* <Typography variant="h5">
            {q.title}
          </Typography>
          <Typography variant="h6" color="gray">
            {q.title}
          </Typography> */}
        </>
      :
        <MChoiceQ
          question={q as FormMultipleChoiceQuestion}
        />
      }

      <Divider sx={{pt: 1}}/>

      </Box>
    })}
  </>
}



export default NonEditableAnswers
