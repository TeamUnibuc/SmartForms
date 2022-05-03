import React, { useState } from "react"

import { Box, Collapse, Grow, List } from "@mui/material"
import { TransitionGroup } from 'react-transition-group';

import { FormDescription } from "~/api/models"
import FormCard from "./FormCard";
import ArrowStateDrawer from "./ArrowStateDrawer";

interface CFDrawerProps
{
  forms: FormDescription[],
  title: string
}

const CustomFormsDrawer = ({forms, title}: CFDrawerProps) =>
{
  const [checked, setChecked] = useState(false);
  const [displayState, setDisplayState] = useState(false)

  const transitionEnd = (e: any) => {
    if (e.propertyName !== 'opacity') return

    if (displayState && !checked)
      setDisplayState(!displayState)
  }

  return <Box style={{display: 'flex', justifyItems: 'center', alignContent: 'center', alignItems: 'center', flexDirection: 'column'}}>

  <ArrowStateDrawer
    text={title}
    state={checked}
    flipState={() => {
      if (!displayState && !checked)
        setDisplayState(!displayState)
      setChecked(!checked)
    }}
  />

  <Box sx={{p: 0}} style={{display: displayState ? 'block' : 'none'}}>
  <Grow in={checked} onTransitionEnd={transitionEnd}>
    <List sx={{pb: 0}} >
      <TransitionGroup style={{display: 'flex', flexWrap: 'wrap',
    justifyContent: 'space-between'}}>
        {forms.map((item, idx) => (
          <Collapse key={idx}>
            <FormCard formDesc={item} />
          </Collapse>
        ))}
      </TransitionGroup>
    </List>
  </Grow>
  </Box>

</Box>

}

export default CustomFormsDrawer
