import { Button, Card, CardActions, CardContent, Typography } from "@mui/material"
import { FormDescription } from "~/api/models"
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

interface FormCardProps
{
  formDesc: FormDescription
}

const FormCard = (props: FormCardProps) => {
  const fDesc = props.formDesc

  return <Card  variant="outlined" sx={{m: 1, boxShadow: 5}}>
    <CardContent>
      <Typography variant="h5" component="div">
        {fDesc.title}
      </Typography>
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
    <CardActions style={{justifyContent: 'center'}}>
      <Button size="small">
        <OpenInNewIcon sx={{mr: 1}}/>
        Learn More
      </Button>
    </CardActions>
  </Card>
}

export default FormCard
