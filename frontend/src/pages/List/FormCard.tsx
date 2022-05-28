import { Box, Button, Card, CardActions, CardContent, Typography } from "@mui/material"
import { FormDescription } from "~/api/models"
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import AddBoxOutlinedIcon from '@mui/icons-material/AddBoxOutlined';
import CircleIcon from '@mui/icons-material/Circle';
import FormatListNumberedIcon from '@mui/icons-material/FormatListNumbered';

import { Link } from "react-router-dom";

interface FormCardProps
{
  formDesc: FormDescription
}

const FormCard = (props: FormCardProps) => {
  const fDesc = props.formDesc

  return <Card
      variant="outlined"
      sx={{boxShadow: 5}}
      style={{width: '100%'}}>
    <CardContent>
      <Box display="flex" justifyContent={'space-between'}>
        <Typography variant="h5" component="div">
          {fDesc.title}
        </Typography>
        <CircleIcon
          color={fDesc.canBeFilledOnline ? "success" : "error"}
          style={{opacity: '85%'}}
        />
      </Box>
      <Typography sx={{ fontSize: 14 }} color="gray" gutterBottom>
        ID: {fDesc.formId}
      </Typography>
      <Typography sx={{ mb: 1.5 }} color="text.secondary">
        {fDesc.description}
      </Typography>
      <Typography variant="body2">
        Nr. of questions: <span style={{fontWeight: 'bold'}}>{fDesc.questions.length}</span>
      </Typography>
    </CardContent>
    <CardActions style={{justifyContent: 'left'}}>
      <Button size="small"
        component={Link}
        sx={{ml: 1, mr: 2}}
        to={`/form?formId=${fDesc.formId}`}>
        <FormatListNumberedIcon sx={{mr: 1}}/>
        Learn More
      </Button>
      <Button size="small"
        component={Link}
        to={`/fast-submit?formId=${fDesc.formId}`}>
        <AddBoxOutlinedIcon sx={{mr: 1}}/>
        Complete Form
      </Button>
    </CardActions>
  </Card>
}

export default FormCard
