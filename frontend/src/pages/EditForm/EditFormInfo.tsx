import { Box, Card, CardContent, TextField, Typography } from "@mui/material"
import { ChangeEvent } from "react"
import { useQLContextState, useQLContextUpdater } from "~/contexts/CoolContext"

const EditFormInfo = () =>
{
  const {title,
         description,
         canBeFilledOnline,
         needsToBeSignedInToSubmit} = useQLContextState()
  const {dOps} = useQLContextUpdater()

  console.log(`Titlu: ${title}`)

  const changeTitle = (e: ChangeEvent<HTMLInputElement>)  => {
    dOps.setTitle(e.target.value)
  }

  const changeDescription = (e: ChangeEvent<HTMLInputElement>)  => {
    dOps.setDesc(e.target.value)
  }

  return <Card raised sx={{mb: 2, p: 1, pb: 0}}>
  <CardContent>
    <TextField required defaultValue={title}
      id="Title" label="Form Title here"
      variant="filled" margin="normal"
      onChange={changeTitle}
      sx={{m: 0, mb: 3}}
      style={{width: "100%"}}
    />

    <TextField defaultValue={description}
      id="form-desc" label="Form Description"
      variant="outlined" margin="normal"
      onChange={changeDescription}
      sx={{m: 0}}
      style={{width: "100%"}}
    />
  </CardContent>
  </Card>
}

export default EditFormInfo
