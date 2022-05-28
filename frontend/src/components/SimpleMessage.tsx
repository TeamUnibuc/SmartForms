import { Alert, AlertColor, Typography } from "@mui/material"

interface SMProps
{
  msg: string
  color: AlertColor
}

const SimpleMessage = ({msg, color}: SMProps) =>
{
  return <Alert severity={color}>
    <Typography>{msg}</Typography>
  </Alert>
}

export default SimpleMessage
