import { Button, Card, CardActions, CardContent, Typography } from "@mui/material"
import React, { useEffect, useState } from "react"
import { Form } from "~/api/form"
import { FormAnswers } from "~/api/models"

interface AnswerCheckProps
{
  answer: FormAnswers
  openModal(): void
}

export default function AnswerCheck(props: AnswerCheckProps): JSX.Element
{
  const [formTitle, setFormTitle] = useState("")

  useEffect(() => {
    const formGetter = async () => {
      const data = await Form.Description(props.answer.formId)
      setFormTitle(data.title)
    }

    formGetter()
  }, [])

  return <Card>
    <CardContent>
      <Typography variant="h5" component="div">
        {formTitle}
      </Typography>
      <Typography sx={{ mb: 1.5 }} color="text.secondary">
        adjective
      </Typography>
      <Typography variant="body2">
        well meaning and kindly.
        <br />
        {'"a benevolent smile"'}
      </Typography>
    </CardContent>
    <CardActions>
      <Button size="small" variant="contained">
        View/Edit Answers
      </Button>
    </CardActions>
  </Card>
}
