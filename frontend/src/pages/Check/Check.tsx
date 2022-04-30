import React, { useState } from 'react'

import { Box, Modal } from '@mui/material'
import { FormAnswers } from '~/api/models'
import AnswerCheck from '~/components/Checking/AnswerCheck'

export interface CheckProps
{
  answers: FormAnswers[]
}

export default function Check(props: CheckProps): JSX.Element
{
  const [modelOpen, setModalOpen] = useState(false)
  const [inferenceDone, setInferenceDone] = useState(false)

  const fnOpenModal = () => {
    if (modelOpen)
      return
    setModalOpen(true)
  }

  const fnCloseModal = () => {
    setModalOpen(false)
  }

  const CheckAnswerCards = () => {
    const lista = props.answers.map((ans, i) => <>
      <AnswerCheck answer={ans} key={i}
          openModal={fnOpenModal}/>
    </>)

  }

  return <>
    {CheckAnswerCards()}
    <Modal
      open={modelOpen}
      onClose={fnCloseModal}
    >
      <Box>
        <p>Some modal</p>
      </Box>
    </Modal>
  </>
}
