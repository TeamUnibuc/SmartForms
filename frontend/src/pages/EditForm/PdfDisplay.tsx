import { useContext } from 'react'
import { Document, Page } from 'react-pdf'
import { QuestionList } from '~/contexts/QuestionList'

export default function PdfDisplay(props: {pdfb64?: string}): JSX.Element
{
  const qlContext = useContext(QuestionList)
  const {pdfString} = qlContext.pdfData

  const embed_string = `data:application/pdf;base64,${pdfString}`

  console.log(`R - pdfDisplay: ${pdfString.length}`)

  return <>
     {pdfString.length > 0 ? (
        <div>
          <embed src={embed_string} type="application/pdf" width="100%" height="900px"></embed>

        </div>
      ) : (
        <p>Nothing loaded so far</p>
      )}
  </>
}
