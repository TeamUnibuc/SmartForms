import React from "react"

import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown'
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight'
import { Box, IconButton, Typography } from "@mui/material"
import { css } from '@emotion/react'
import { makeStyles, withStyles } from 'tss-react/mui'

interface ASDProps
{
  state: boolean
  flipState(): void
  text?: string
}

const ArrowStateDrawer = ({state, flipState, text}: ASDProps) =>
{
  const icon = state ? <KeyboardArrowDownIcon sx={{fontSize: 32}}/> : <KeyboardArrowRightIcon sx={{fontSize: 32}}/>

  return <Box width='100%' style={{display: 'flex', alignItems: "center"}}>
  <Typography style={{verticalAlign: 'middle'}}>
    <IconButton
      sx={{p: 0}}
      onClick={flipState}
      style={{display: 'inline-block'}}
    >
      {icon}
    </IconButton>

    <span style={{color: 'gray'}}>
      {text}
    </span>

  </Typography>
</Box>
}

// const useStyle = makeStyles()({
//   "arrText": {
//     'display': 'flex',
//     'flexDirection': 'row',
//     'color': 'gray',
//     'height': '100%',

//     '&:before, &:after': {
//       'content': '""',
//       'borderBottom': '1px solid',
//       'margin': 'auto'
//     },
//     '&:before': {
//       'flex': '10',
//       'marginRight': '4px'
//     },
//     '&:after': {
//       'flex': '90',
//       'marginLeft': '4px'
//     },
//   }
// })

export default ArrowStateDrawer
