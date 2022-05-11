import { Box } from "@mui/material"

interface PDProps
{
  pdfString: string
}

const PdfDisplay = ({pdfString}: PDProps) =>
{
  const embed_string = `data:application/pdf;base64,${pdfString}`

  return <Box>
     {pdfString.length > 0 ? (
        <div>
          <embed src={embed_string} type="application/pdf" width="100%" height="900px"></embed>

        </div>
      ) : (
        <p>Nothing loaded so far</p>
      )}
  </Box>
}

export default PdfDisplay
