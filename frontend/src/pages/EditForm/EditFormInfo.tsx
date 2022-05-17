import { Box, Card, CardContent, Switch, TextField, Typography } from "@mui/material"
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

  const fillClick = ()  => {
    dOps.setFillOnline(!canBeFilledOnline)
  }


  const signedSubmitClick = ()  => {
    dOps.setFillOnline(!needsToBeSignedInToSubmit)
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

    <Box display="flex" style={{alignItems: "center"}} sx={{mb: 1, mt: 2}}>
      <Switch
        checked={canBeFilledOnline}
        onChange={fillClick}
      />
      <Typography sx={{ml: 2}}>
        Can the form receive answers?
      </Typography>
    </Box>

    <Box display="flex" style={{alignItems: "center"}} sx={{mb: 1}}>
      <Switch
        checked={needsToBeSignedInToSubmit}
        onChange={signedSubmitClick}
      />
      <Typography sx={{ml: 2}}>
        Require authenticateed users?
      </Typography>
    </Box>

  </CardContent>
  </Card>
}

export default EditFormInfo
