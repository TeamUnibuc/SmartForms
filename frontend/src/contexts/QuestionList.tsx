import React, { FunctionComponent, useState } from 'react'
import { Question } from '~/api/models'

interface QLCType {
  qList: {
    questions: Question[],
    setQuestion: (q_ind: number, q: Question) => void,
    addQuestion: (q: Question) => void
    delQuestion: () => void
  },
  pdfData: {
    pdfString: string,
    setPdfString: React.Dispatch<React.SetStateAction<string>>
  }
}

const QuestionList = React.createContext<QLCType>({
  qList: {
    questions: [],
    setQuestion: () => {},
    addQuestion: () => {},
    delQuestion: () => {}
  },
  pdfData: {
    pdfString: '',
    setPdfString: () => {}
  }
})

const QuestionListProvider: React.FC = (props) =>
{
  console.log("R - QL Provider")

  const [questions, setQuestions] = useState<Question[]>([])
  const [pdfString, setPdfString] = useState('')

  console.log("Init question array")
  const setQuestion = (q_ind: number, q: Question) => {
    console.log(`Array len: ${questions.length}`)
    questions[q_ind] = q
    setQuestions(questions)
  }
  const addQuestion = (newq: Question) => {
    questions.push(newq)
    setQuestions(questions)
  }
  const delQuestion = () => {
    questions.pop()
    setQuestions(questions)
  }

  const qList = {questions, setQuestion, addQuestion, delQuestion}
  const pdfData = {pdfString, setPdfString}

  return <QuestionList.Provider value={{qList, pdfData}}>
    {props.children}
  </QuestionList.Provider>
}

const QuestionListConsumer = QuestionList.Consumer

export {QuestionListProvider, QuestionListConsumer, QuestionList}
