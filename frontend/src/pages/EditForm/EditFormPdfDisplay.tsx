import React from 'react'
import PdfDisplay from '~/components/PdfDisplay'

import { useQLContextState } from '~/contexts/QLContext'

export default function EditFormPdfDisplay(): JSX.Element
{
  const {pdfString} = useQLContextState()

  return <PdfDisplay pdfString={pdfString} />
}
