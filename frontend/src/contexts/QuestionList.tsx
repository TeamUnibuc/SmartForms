import React, { useState } from 'react'
import { Question } from '~/api/models'

interface QLCType {
  qList: {
    questions: (Question | undefined)[],
    setQuestion: (q_ind: number, q: Question) => void,
    addQuestion: (q: Question | undefined) => void
    delQuestion: (index?: number) => void
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

  const [questions, setQuestions] = useState<(Question | undefined)[]>([])
  const [pdfString, setPdfString] = useState('')

  console.log("Init question array")
  const setQuestion = (q_ind: number, q: Question) => {
    console.log(`Array len: ${questions.length}`)
    questions[q_ind] = q
    setQuestions(questions)
  }
  const addQuestion = (newq?: Question) => {
    console.log("Adding question in context")
    questions.push(newq)
    setQuestions(questions)
  }
  const delQuestion = (index?: number) => {
    if (index !== undefined && index >= 0 && index < questions.length) {
      for (let i = index; i + 1 < questions.length; ++i) {
        questions[i] = questions[i + 1];
      }
    }
    questions.pop()
    setQuestions(questions)
  }

  const qList = {questions, setQuestion, addQuestion, delQuestion}
  const pdfData = {pdfString, setPdfString}

  return <QuestionList.Provider value={{qList, pdfData}}>
    {props.children}
  </QuestionList.Provider>
}

const useQLQuestions = () =>
{

}


const QuestionListConsumer = QuestionList.Consumer

export {QuestionListProvider, QuestionListConsumer, QuestionList}
