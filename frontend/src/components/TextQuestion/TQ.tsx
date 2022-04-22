import React from 'react'

import { Card, CardActions, IconButton } from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete';
import { FormTextQuestion, Question } from '~/api/models'
import TQMultipleChoice from './TQMultipleChoice'
import TQText from './TQText'
import TQUndefined from './TQUndefined'

function TextQuestion(props:
    {q_ind: number,
     q_content?: Question
    }): JSX.Element
{
  console.log(`Rendering TQ: ${props.q_ind}`)

  let {q_ind, q_content} = props
  const question = q_content

  const getActualCard = () => {
    if (question === undefined)
      return <TQUndefined q_ind={q_ind}/>

    if ( (question as FormTextQuestion).maxAnswerLength !== undefined )
      return <TQText q_ind={q_ind}/>
    else
      return <TQMultipleChoice q_ind={q_ind}/>
  }

  return <Card variant="outlined" sx={{p: 1, m: 1}}>
    {getActualCard()}
    <CardActions>
      <IconButton>
        <DeleteIcon></DeleteIcon>
      </IconButton>
    </CardActions>
  </Card>
}

export default TextQuestion
