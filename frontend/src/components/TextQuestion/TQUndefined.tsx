import { Button, CardActions, CardContent, Typography } from "@mui/material";
import React from "react";

import { useQLContextState, useQLContextUpdater } from "~/contexts/QLContext";

interface ComponentProps
{
  q_ind: number
}

const TQAddText = (props: {action: () => {}}) => {
  return <Button onClick={props.action}>
    Add Text Question
  </Button>
}

const TQAddMultiple = (props: {action: () => {}}) => {
  return <Button onClick={props.action}>
    Add Multiple Choice Question
  </Button>
}

export default function TQUndefined(props: ComponentProps): JSX.Element
{
  const {qList} = useQLContextState()
  const {qOps} = useQLContextUpdater()

  const addText = () =>
  {
    qOps.setQuestion(props.q_ind, {
      allowedCharacters: " ",
      title: `Question ${props.q_ind} title`,
      description: `Description`,
      maxAnswerLength: 5
    })
  }

  const addMultiple = () =>
  {
    qOps.setQuestion(props.q_ind, {
      title: `Question ${props.q_ind} title`,
      description: `Description`,
      choices: [
        'Option 1',
        'Option 2'
      ]
    })
  }

  return <>
    <CardContent>
      <Typography>
        Add a new question. It can be either a text question or multiple hoice.
      </Typography>
    </CardContent>
    <CardActions>
      <Button onClick={addText}>
        Add Text Question
      </Button>
      <Button onClick={addMultiple}>
        Add Multiple Choice Question
      </Button>
    </CardActions>
  </>
}
