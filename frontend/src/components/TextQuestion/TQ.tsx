import React from 'react'

import { Card, CardActions, IconButton } from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete';
import { FormTextQuestion, Question } from '~/api/models'
import TQMultipleChoice from './TQMultipleChoice'
import TQText from './TQText'
import TQUndefined from './TQUndefined'
import { useQLContextUpdater } from '~/contexts/CoolContext';

function TextQuestion(props:
    {q_ind: number,
     q_content?: Question
    }): JSX.Element
{
  console.log(`Rendering TQ: ${props.q_ind}`)

  const {qOps} = useQLContextUpdater()

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

  const delQuestion = () => {
    qOps.delQuestion(props.q_ind)
  }

  return <Card variant="outlined" sx={{m: 1}}>
    {getActualCard()}
  </Card>
}

export default TextQuestion
