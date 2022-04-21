import React from 'react'

import { useQLContextState } from '~/contexts/CoolContext'

export default function PdfDisplay(props: {pdfb64?: string}): JSX.Element
{
  const {pdfString} = useQLContextState()

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
