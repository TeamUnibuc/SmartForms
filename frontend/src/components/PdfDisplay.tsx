import { Box } from "@mui/material"

interface PDProps
{
  pdfString: string
}

const PdfDisplay = ({pdfString}: PDProps) =>
{
  const embed_string = `data:application/pdf;base64,${pdfString}`

  return <Box height="100%" sx={{py: 3}}>
     {pdfString.length > 0 ? (
          <embed src={embed_string} type="application/pdf" width="100%" height="100%"></embed>
      ) : (
        <p>Nothing loaded so far</p>
      )}
  </Box>
}

export default PdfDisplay
