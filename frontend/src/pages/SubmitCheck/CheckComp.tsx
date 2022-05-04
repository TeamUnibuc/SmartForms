import { Alert, AlertColor, Box, Button, Collapse, Divider, IconButton, Modal, SxProps, Typography } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';

import { useState } from "react";
import API from "~/api";
import { FormAnswers } from "~/api/models";
import FormCardCheck, { ModalDataType } from "./FormCardCheck";
import ModalCard from "./ModalCard";

const CheckComp = (props: {
    answers: FormAnswers[],
    setAnswers(anss: FormAnswers[]): void
}) =>
{
  console.log("Rendered Answers")
  console.log(props.answers)

  const [alertOpen, setAlertOpen] = useState(false)
  const [alertContent, setAlertContent] = useState<{msg: string, severity: AlertColor}>({severity: "info", msg: ""})
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

  const submitButton = () =>
  {
    let totalSent = 0

    const showSentAlert = () =>
    {
      if (totalSent == props.answers.length)
        setAlertContent({
          severity: "success",
          msg: "All entries submitted!"
        })
      else if (totalSent > 0)
        setAlertContent({
          severity: "warning",
          msg: `Could only send ${totalSent}/${props.answers.length} entries :/`
        })
      else
        setAlertContent({
          severity: "error",
          msg: "Something has gone terribly wrong :("
        })

      setAlertOpen(true)
    }

    Promise.all(props.answers.map(ans =>
      API.Entry.Edit(ans)
      .then(r => {
        totalSent += 1
        return r
      })
    ))
    .catch(e => {
      console.log("Error sending entries")
      console.log(e)
    }).finally(() => showSentAlert())
  }

  return <Box>
    <ModalCard
        data={modalData}
        open={open}
        setModalClose={setModalClose}
        setModalData={d => setModalData(d)}
    />

    <Box sx={{display: 'flex'}}>
      {getLista()}
    </Box>

    <Divider sx={{m: 1}} orientation="horizontal"/>

    <Button variant="contained" color="success"
      onClick={submitButton}
    >
      Confirm Answers
    </Button>

    <Box sx={{ width: '100%' }}>
      <Collapse in={alertOpen}>
        <Alert severity={alertContent.severity}
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setAlertOpen(false);
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
          {alertContent.msg}
        </Alert>
      </Collapse>
    </Box>
  </Box>
}

export default CheckComp
