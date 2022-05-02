import { Button, Card, CardActions, CardContent, Typography } from "@mui/material"
import { FormDescription } from "~/api/models"

interface FormCardProps
{
  formDesc: FormDescription
}

const FormCard = (props: FormCardProps) => {
  const fDesc = props.formDesc
  console.log(fDesc)
  console.log(`rendering form: ${fDesc.title} - ${fDesc.formId}`)

  return <Card variant="outlined" sx={{m: 1}}>
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
        Nr. of questions: {fDesc.questions.length}
      </Typography>
    </CardContent>
    <CardActions style={{justifyContent: 'center'}}>
      <Button size="small">Learn More</Button>
    </CardActions>
  </Card>
}

export default FormCard
