import { Button, Card, CardActions, CardContent, Typography } from "@mui/material"
import { FormDescription } from "~/api/models"

interface FormCardProps
{
  formDesc: FormDescription
}

const FormCard = ({formDesc: fDesc}: FormCardProps) => {
  console.log(`rendering form: ${fDesc.title} - ${fDesc.formID}`)
  return <Card variant="outlined">
    <CardContent>
      <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
        {fDesc.formID}
      </Typography>
      <Typography variant="h5" component="div">
        {fDesc.title}
      </Typography>
      <Typography sx={{ mb: 1.5 }} color="text.secondary">
        {fDesc.description}
      </Typography>
      <Typography variant="body2">
        Nr. of questions: {fDesc.questions.length}
      </Typography>
    </CardContent>
    <CardActions>
      <Button size="small">Learn More</Button>
    </CardActions>
  </Card>
}

export default FormCard
