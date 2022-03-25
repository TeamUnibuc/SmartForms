import { Document, Page } from 'react-pdf'

export default function PdfDisplay(props: {pdfb64?: string}): JSX.Element
{
  const embed_string = `data:application/pdf;base64,${props.pdfb64}`

  return <>
     {props.pdfb64 ? (
        <div>
          <embed src={embed_string} type="application/pdf" width="100%" height="900px"></embed>

        </div>
      ) : (
        <p>Nothing loaded so far</p>
      )}
  </>
}
