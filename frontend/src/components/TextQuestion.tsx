import TextField from '@mui/material/TextField'
import React, { ChangeEvent, useContext, useEffect, useState } from 'react'

import { FormTextQuestion, Question } from '~/api/models'
import { QuestionList, QuestionListConsumer, QuestionListProvider } from '~/contexts/QuestionList'

function TextQuestion(props:
    {q_ind: number,
    //  q_updater: (q: Question) => void
    }): JSX.Element
{
  const {q_ind} = props

  const [question, setQuestion] = useState<FormTextQuestion>({
    title: `Question ${q_ind}`,
    description: ``,
    maxAnswerLength: 5
  })

  useEffect(() => {
    console.log(`Effect for question ${q_ind}`)
    qlConsumer.qList.setQuestion(q_ind - 1, question)
  }, [])

  const qlConsumer = useContext(QuestionList)

  console.log("R - TQ - ql")
  console.log(qlConsumer.qList.questions)

  const myUpdateQ = (q: FormTextQuestion) => {
    console.log("Updating a question")
    setQuestion(q)
    qlConsumer.qList.setQuestion(q_ind - 1, q)
  }

  const changeQuestionTitle = (e: ChangeEvent<HTMLInputElement>)  => {
    const newq = {...question, title: e.target.value}
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

  console.log(`R - TextQuestion ${q_ind}`)

  return <>
    <TextField required defaultValue={question.title}
      id="first-question-title" label="Question title"
      variant="filled" margin="normal"
      onChange={changeQuestionTitle}/>
    <TextField defaultValue={question.description}
      id="first-question-content" label="Question description"
      variant="filled" margin="normal"
      onChange={changeQuestionContent}/>
    <TextField required defaultValue={question.maxAnswerLength}
      id="first-question-length" label="Answer length"
      variant="filled" margin="normal" type='number'
      onChange={changeQuestionLength}/>

    {/* <QuestionListConsumer >
      {q_list => {
        console.log(`Content of node ${q_ind}: `)
        console.log(q_list[q_ind])
        return <div>

        </div>
      }}
    </QuestionListConsumer> */}
  </>
}

export default TextQuestion
