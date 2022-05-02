import { Box, Collapse, List } from "@mui/material"
import { FormDescription } from "~/api/models"
import { TransitionGroup } from 'react-transition-group';
import FormCard from "./FormCard";

interface CFDrawerProps
{
  forms: FormDescription[],
  title: string
}

const CustomFormsDrawer = ({forms, title: _title}: CFDrawerProps) =>
{
  return <Box sx={{ mt: 1, display: 'flex', width: '100%' }}>
  {/* <List> */}
    {/* <TransitionGroup> */}
      {forms.map((item, idx) => (
        <Collapse key={idx}>
          <FormCard formDesc={item} />
        </Collapse>
      ))}
    {/* </TransitionGroup> */}
  {/* </List> */}
</Box>
}

export default CustomFormsDrawer
