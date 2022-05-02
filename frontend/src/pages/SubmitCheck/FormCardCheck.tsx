import { Box, Card, CardActionArea, CardContent, CardActions, Typography, Button } from "@mui/material"
import { useEffect, useState } from "react"
import API from "~/api"
import { FormAnswers, FormDescription } from "~/api/models"

export type ModalDataType = undefined | {
  fAns: FormAnswers
  fDesc: FormDescription
  modalFnUpdater(ans: FormAnswers): void
}

const FormCardCheck = (props: {
    answer: FormAnswers,
    idx: number,
    openModal(): void,
    setModalData(d: ModalDataType): void,
    setNthAnswer(idx: number, ans: FormAnswers): void
}) =>
{
  const [formInfo, setFormInfo] = useState<undefined | FormDescription>()
  const [cardTitle, setCardTitle] = useState(props.answer.formId)

  useEffect(() => {
    const sleep = (time: number) => {
      return new Promise((resolve) => setTimeout(resolve, time));
    }

    const getInfo = async () => {
      const data = await API.Form.Description(props.answer.formId)
      await sleep(600)
      setFormInfo(data)
      setCardTitle(data.title)
    }

    getInfo()
  }, [])

  const viewEditClick = () => {
    if (formInfo) {
      props.setModalData({
        fAns: props.answer,
        fDesc: formInfo,
        modalFnUpdater: (content) => {
          props.setNthAnswer(props.idx, content)
        }
      })
      props.openModal()
    }
  }

  return <Card style={{minWidth: "15em"}} sx={{m: 1}}>
    <CardActionArea>
      <CardContent>
      <Typography gutterBottom variant="h5" component="div">
        <span style={{color: "gray"}}>
          #{props.idx + 1 + " "}
        </span>
        {cardTitle}
      </Typography>
      <Typography>
        <span style={{color: "gray"}}>Answers: </span>
        {props.answer.answers.length}
      </Typography>
      </CardContent>
    </CardActionArea>
    <CardActions>
      <Box textAlign='center' width='100%'>
        <Button variant="outlined" onClick={viewEditClick}>
          View / Edit
        </Button>
      </Box>
    </CardActions>
  </Card>
}

export default FormCardCheck
