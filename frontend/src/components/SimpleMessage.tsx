import { Alert, AlertColor, Box, Typography } from "@mui/material"

interface SMProps
{
  msg: string
  color: AlertColor
}

const SimpleMessage = ({msg, color}: SMProps) =>
{
  return <Box display="flex" justifyContent='center'>
    <Alert severity={color}>
      <Typography>{msg}</Typography>
    </Alert>
  </Box>

}

export default SimpleMessage
