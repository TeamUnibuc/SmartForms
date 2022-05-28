import { Box, Dialog, DialogContent, DialogTitle, Modal, SxProps, Typography } from "@mui/material"
import { SingleQAnswer } from "~/api/models"
import EditableAnswers from "../../components/EditableAnswers"

import { ModalDataType } from "./FormCardCheck"

interface ModalCardProps
{
  data: ModalDataType
  open: boolean
  setModalClose(): void
  setModalData(d: ModalDataType): void
}

const ModalCard = ({data, open, setModalClose, setModalData}: ModalCardProps) =>
{
  const style: SxProps = {
    // width: 'max(50px, 60px)',
    // width: '100%',
    bgcolor: 'background.paper',
    // border: '2px solid #000',
    boxShadow: 24,
    // overflow: "scroll",
    p: 3,
  };

  return <Dialog
    open={open}
    onClose={setModalClose}
    aria-labelledby="modal-modal-title"
    aria-describedby="modal-modal-description"
    fullWidth={true}
    maxWidth={"md"}
  >
  <DialogContent sx={style}>
  {data === undefined ?
    <Typography>
      Error loading information, try reopening
    </Typography>
    :
    <Box>
      <Typography variant="h6" component="h2">
        <span style={{color: "gray"}}>Title: </span>
        {data.fDesc.title}
      </Typography>
      <Typography sx={{ mt: 1 }} fontSize={'0.9rem'}>
        <span style={{color: "gray"}}>Form ID: </span>
        {data.fAns.formId}
      </Typography>
      <Typography sx={{ mt: 1 }} fontSize={'0.9rem'}>
        <span style={{color: "gray"}}>Answer ID: </span>
        {data.fAns.answerId}
      </Typography>
      <Typography id="modal-modal-description" sx={{ mt: 1 }}>
        <span style={{color: "gray"}}>Answers: </span>
        {data.fAns.answers.length}
      </Typography>

      <EditableAnswers
        answers={data.fAns.answers}
        questions={data.fDesc.questions}
        updater={(answers: SingleQAnswer[]) => {
            data.modalFnUpdater({...data.fAns, answers: answers})
            setModalData({...data, fAns: {...data.fAns, answers: answers}})
        }}
      />

    </Box>}
  </DialogContent>
  </Dialog>

}

export default ModalCard
