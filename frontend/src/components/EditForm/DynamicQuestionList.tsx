import React from "react"

import { Divider } from "@mui/material";
import { useQLContextState } from "~/contexts/QLContext";
import TQ from "../TextQuestion/TQ";
import TQAdd from "../TextQuestion/TQAdd";

export default function DynamicQuestionList(): JSX.Element
{
  const {qList} = useQLContextState()
  const questions = qList.questions;

  console.log(`Rendering dynamic list, length questions: ${questions.length}`);

  const getCompList = (): JSX.Element =>
  {
    const lista = qList.questions.map((q, i) => {
      return <TQ q_ind={i} q_content={q} key={i}/>
    })

    return <>
      {lista}
    </>
  }

  return <>
    {getCompList()}
    <Divider orientation="horizontal"/>
    <TQAdd/>
  </>
}
