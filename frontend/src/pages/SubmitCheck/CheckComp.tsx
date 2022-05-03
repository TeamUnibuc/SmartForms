import { Box, Button, Divider, Modal, SxProps, Typography } from "@mui/material";
import { useState } from "react";
import { FormAnswers } from "~/api/models";
import FormCardCheck, { ModalDataType } from "./FormCardCheck";
import ModalCard from "./ModalCard";

const CheckComp = (props: {
    answers: FormAnswers[],
    setAnswers(anss: FormAnswers[]): void
}) =>
{
  console.log("Original Answers")
  console.log(props.answers)

  const [open, setOpen] = useState(false);
  const [modalData, setModalData] = useState<ModalDataType>(undefined)
  const setModalOpen = () => setOpen(true);
  const setModalClose = () => setOpen(false);

  const setNthAnswer = (idx: number, ans: FormAnswers) =>
  {
    const newAnswers = [...props.answers]
    newAnswers[idx] = ans
    props.setAnswers(newAnswers)
  }

  const tryOpenModal = () => {
    if (open)
      return
    setModalOpen()
  }

  const getLista = () => {
    return props.answers.map((ans, i) => {
      return <FormCardCheck
        answer={ans}
        openModal={tryOpenModal}
        setModalData={d => setModalData(d)}
        setNthAnswer={setNthAnswer}
        key={i} idx={i}/>
    })
  }

  return <Box>
    <ModalCard
        data={modalData}
        open={open}
        setModalClose={setModalClose}
    />

    <Box sx={{display: 'flex'}}>
      {getLista()}
    </Box>

    <Divider sx={{m: 1}} orientation="horizontal"/>

    <Button variant="contained" color="success">
      Submit Answers
    </Button>
  </Box>
}

export default CheckComp
