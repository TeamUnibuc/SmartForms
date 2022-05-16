import { Box, Button, Typography,  Switch } from "@mui/material"
import { useState } from "react";
import API from "~/api"
import { FormDescription } from "~/api/models";

interface OCProps
{
  formId: string,
  snack: [
    React.Dispatch<React.SetStateAction<boolean>>,
    React.Dispatch<React.SetStateAction<{
        msg: string;
        sev: string;
    }>>],
  formData: FormDescription
}

const Settings = ({formId, snack, formData}: OCProps) =>
{
  const [setSnackOpen, setSnackState] = snack
  const [restrictOnlyUsers, setRestrictOnlyUsers] = useState(formData.needsToBeSignedInToSubmit);
  const [restrictCanFill, setRestrictCanFill] = useState(formData.canBeFilledOnline);

  const deleteClick = async () =>
  {
    const rez = await API.Form.Delete(formId)
      .then(r => {
        setSnackState({msg: "Form deleted!", sev: "success"})
      })
      .catch(e => {
        setSnackState({msg: "Error occured :/", sev: "error"})
      })
      .finally(() => {
        setSnackOpen(true)
      })
  }

  const canFillClick = () =>
  {
    API.Form.OnlineAccess(formId, {
      canBeFilledOnline: !restrictCanFill,
      needsToBeSignedInToSubmit: restrictOnlyUsers})
    .then(r => {
      setSnackState({msg: "Update saved!", sev: "success"})
    })
    .catch(e => {
      setSnackState({msg: "Unable to update :/", sev: "error"})
    })
    .finally(() => {
      setSnackOpen(true)
    })

    setRestrictCanFill(!restrictCanFill)
  }

  const onlyUsersClick = () =>
  {
    API.Form.OnlineAccess(formId, {
      canBeFilledOnline: restrictCanFill,
      needsToBeSignedInToSubmit: !restrictOnlyUsers})
    .then(r => {
      setSnackState({msg: "Update saved!", sev: "success"})
    })
    .catch(e => {
      setSnackState({msg: "Unable to update :/", sev: "error"})
    })
    .finally(() => {
      setSnackOpen(true)
    })

    setRestrictOnlyUsers(!restrictOnlyUsers)
  }

  return <Box>
    <Typography color="#a1c9c5" variant="h6" sx={{mb: 2}} style={{fontWeight: 500}}>
      Form Settings:
    </Typography>

    <Box display="flex" style={{alignItems: "center"}} sx={{mb: 1}}>
      <Switch
        checked={restrictCanFill}
        onChange={canFillClick}
      />
      <Typography sx={{ml: 2}}>
        Is form available to receive answers?
      </Typography>

    </Box>

    <Box display="flex" style={{alignItems: "center"}} sx={{mb: 1}}>
      <Switch
        checked={restrictOnlyUsers}
        onChange={onlyUsersClick}
      />
      <Typography sx={{ml: 2}}>
        Do users need to be signed in to complete the form?
      </Typography>
    </Box>

    <Typography color="#a1c9c5" variant="h6" sx={{mb: 2}} style={{fontWeight: 500}}>
      Form Commands:
    </Typography>
    <Button color="error" variant="contained" onClick={deleteClick}>
      Delete
    </Button>
  </Box>
}

export default Settings
