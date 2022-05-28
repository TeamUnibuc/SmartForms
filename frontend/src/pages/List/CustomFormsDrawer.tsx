import React, { useEffect, useState } from "react"

import { Box, Collapse, Grow, List, Typography, useTheme } from "@mui/material"
import { TransitionGroup } from 'react-transition-group';

import { FormDescription } from "~/api/models"
import FormCard from "./FormCard";
import ArrowStateDrawer from "./ArrowStateDrawer";

interface CFDrawerProps
{
  forms: FormDescription[]
  title: string
  openDelay?: number
}

const CustomFormsDrawer = ({forms, title, openDelay}: CFDrawerProps) =>
{
  const [checked, setChecked] = useState(false)
  const [displayState, setDisplayState] = useState(false)
  const {palette} = useTheme()

  const transitionEnd = (e: any) => {
    if (e.propertyName !== 'opacity') return

    if (displayState && !checked)
      setDisplayState(!displayState)
  }

  const flipAction = () =>
  {
    if (!displayState && !checked)
      setDisplayState(!displayState)
    setChecked(!checked)
  }

  useEffect(() => {
    if (openDelay !== undefined)
      setTimeout(() => flipAction(), openDelay)
  }, [])

  return <Box style={{display: 'flex', justifyItems: 'center', alignContent: 'center', alignItems: 'center', flexDirection: 'column'}}>

  <ArrowStateDrawer
    text={title}
    state={checked}
    flipState={flipAction}
  />

  <Box
      sx={{p: 0}}
      style={{display: displayState ? 'block' : 'none'}}
      width='100%'>
  <Collapse in={checked} onTransitionEnd={transitionEnd}>
    <List sx={{pb: 0}} >
      <TransitionGroup style={{
        // display: 'flex',
        // flexWrap: 'wrap',
        // justifyContent: 'space-between'
      }}>
        <Box display='flex' width='100%'
          style={{flexWrap: 'wrap'}}>
          {forms.map((item, idx) => (
            <Box sx={{p: 2}} width='100%' maxWidth={'50%'} style={{flex: '50%'}}>
              <FormCard formDesc={item}/>
            </Box>
          ))}
        </Box>
      </TransitionGroup>
    </List>
  </Collapse>
  </Box>

</Box>

}

export default CustomFormsDrawer
