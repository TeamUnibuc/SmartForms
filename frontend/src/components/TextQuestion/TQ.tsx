import React from 'react'

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

  if (question === undefined)
    return <TQUndefined q_ind={q_ind}/>

  if ( (question as FormTextQuestion).maxAnswerLength !== undefined )
    return <TQText q_ind={q_ind}/>
  else
    return <TQMultipleChoice q_ind={q_ind}/>
}

export default TextQuestion
