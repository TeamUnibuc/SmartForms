import { Box, Button, Divider, Modal, Typography } from "@mui/material";
import { useState } from "react";
import { FormAnswers } from "~/api/models";
import FormCardCheck, { ModalDataType } from "./FormCardCheck";

const CheckComp = (props: {answers: FormAnswers[]}) =>
{
  const [open, setOpen] = useState(false);
  const [modalData, setModalData] = useState<ModalDataType>(undefined)
  const setModalOpen = () => setOpen(true);
  const setModalClose = () => setOpen(false);

  const tryOpenModal = () => {
    if (open)
      return
    setModalOpen()
  }

  const style = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

  const getLista = () => {
    return props.answers.map((ans, i) => {
      return <FormCardCheck
        answer={ans}
        openModal={tryOpenModal} setModalData={d => setModalData(d)}
        key={i} idx={i}/>
    })
  }

  return <Box>
    <Modal
      open={open}
      onClose={setModalClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
      {modalData === undefined ?
        <Typography>Weird, this shouldnt happend</Typography>
       : <>
        <Typography id="modal-modal-title" variant="h6" component="h2">
          {modalData.fDesc.title}
        </Typography>
        <Typography id="modal-modal-description" sx={{ mt: 2 }}>
          {modalData.fAns.formId}
        </Typography>
       </>
      }

      </Box>
    </Modal>

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
