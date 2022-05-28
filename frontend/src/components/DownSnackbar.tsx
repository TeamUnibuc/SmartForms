import { Alert, AlertColor, Snackbar } from "@mui/material"
import { useState } from "react"

interface DSProps
{
  onClose?(event: React.SyntheticEvent | Event, reason?: string): void
  color?: AlertColor
  msg?: string
  initShow?: boolean
}

const DownSnackbar = ({
  onClose: prop_onClose,
  color = "info",
  msg = "---",
  initShow = false
}: DSProps) =>

{
  const [snackOpen, setSnackOpen] = useState(!!initShow)

  const defaultOnClose = (event: React.SyntheticEvent | Event, reason?: string) =>
  {
    if (reason === 'clickaway') {
      return;
    }

    setSnackOpen(false);
  }
  const onClose = prop_onClose || defaultOnClose

  return <Snackbar
    anchorOrigin={{vertical: 'bottom', horizontal: 'center'}}
    open={snackOpen}
    autoHideDuration={5000}
    onClose={onClose}
  >
    <Alert
      onClose={onClose}
      severity={color}
      sx={{ width: '100%' }}
    >
      {msg}
    </Alert>
  </Snackbar>
}

export default DownSnackbar
