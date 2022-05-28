import React from "react"

import { Button } from "@mui/material";
import { useQLContextState, useQLContextUpdater } from "~/contexts/CoolContext";

const TQAddText = (props: {action: () => void}) => {
  return <Button variant="contained" onClick={props.action} sx={{m: 1}}>
    Add Text Question
  </Button>
}

const TQAddMultiple = (props: {action: () => void}) => {
  return <Button variant="contained" onClick={props.action} sx={{m: 1}}>
    Add Multiple Choice Question
  </Button>
}

export default function TQAdd(): JSX.Element
{
  const {qList} = useQLContextState()
  const {qOps} = useQLContextUpdater()

  const getNextInd = () => {
    return qList.questions.length;
  }

  const addText = () =>
  {
    const q_ind = getNextInd()
    qOps.setQuestion(q_ind, {
      title: `Text ${q_ind} title`,
      description: ``,
      maxAnswerLength: 5
    })
  }

  const addMultiple = () =>
  {
    const q_ind = getNextInd()
    qOps.setQuestion(q_ind, {
      title: `Multiple ${q_ind} title`,
      description: ``,
      choices: [
        'Option 1',
        'Option 2'
      ]
    })
  }

  return <>
    <TQAddText action={addText} />
    <TQAddMultiple action={addMultiple} />
  </>
}
