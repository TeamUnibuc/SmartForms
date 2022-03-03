import { Document, Page } from 'react-pdf'

export default function PdfDisplay(props: {pdfb64?: string}): JSX.Element
{
  return <>
    <div></div>
     {props.pdfb64 ? (
        <Document file={props.pdfb64}>
        </Document>
      ) : (
        <p>Nothing loaded so far</p>
      )}
  </>
}
