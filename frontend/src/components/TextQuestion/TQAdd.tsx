import { Button } from "@mui/material";
import React from "react"

import { useQLContextState, useQLContextUpdater } from "~/contexts/CoolContext";

export default function TQAdd(): JSX.Element
{
  const {qOps} = useQLContextUpdater();

  const addEvent = () =>
  {
    console.log("Button to add question pressed")
    qOps.addQuestion(undefined)
  }

  return <Button variant="contained" onClick={addEvent}>
    ADD QUESTION
  </Button>
}
