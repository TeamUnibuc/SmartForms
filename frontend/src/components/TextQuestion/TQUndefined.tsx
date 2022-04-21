import React from "react";

import { Button, CardActions, CardContent, Typography } from "@material-ui/core";
import { Card } from "@mui/material";
import { useQLContextState, useQLContextUpdater } from "~/contexts/CoolContext";

interface ComponentProps
{
  q_ind: number
}

export default function TQUndefined(props: ComponentProps): JSX.Element
{
  const {qList} = useQLContextState()
  const {qOps} = useQLContextUpdater()

  const addText = () =>
  {
    qOps.setQuestion(props.q_ind, {
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

  return <Card variant="outlined" sx={{m: 1}}>
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
  </Card>
}
