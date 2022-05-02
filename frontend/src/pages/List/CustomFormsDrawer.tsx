import React from "react"

import { Box, Collapse, Fade, FormControlLabel, Grow, List, Switch } from "@mui/material"
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
  const [checked, setChecked] = React.useState(false);

  const handleChange = () => {
    setChecked((prev) => !prev);
  };

  return <Box style={{display: 'flex', justifyItems: 'center', alignContent: 'center', alignItems: 'center', flexDirection: 'column'}}>

  <ArrowStateDrawer
    text={title}
    state={checked}
    flipState={() => setChecked(!checked)}
  />

  <Box sx={{p: 0}} >
  <Grow in={checked}>
    <List sx={{pb: 0}}>
      <TransitionGroup style={{display: 'flex'}}>
        {forms.map((item, idx) => (
          <Collapse key={idx}>
            {!checked ? <></> :
            <FormCard key={idx} formDesc={item} />}
          </Collapse>
        ))}
      </TransitionGroup>
    </List>
  </Grow>
  </Box>

</Box>

}

export default CustomFormsDrawer
