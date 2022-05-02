import { Box, Dialog, DialogContent, DialogTitle, Modal, SxProps, Typography } from "@mui/material"

import { ModalDataType } from "./FormCardCheck"

interface ModalCardProps
{
  data: ModalDataType
  open: boolean
  setModalClose(): void
}

const ModalCard = ({data, open, setModalClose}: ModalCardProps) =>
{
  const style: SxProps = {
    // position: 'absolute',
    // top: '50%',
    // left: '50%',
    // transform: 'translate(-50%, -50%)',
    // width: 400,
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



    </Box>}
  </DialogContent>
  </Dialog>

}

export default ModalCard
