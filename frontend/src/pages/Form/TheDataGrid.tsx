import { useEffect, useState } from "react"
import { FormAnswers, FormDescription } from "~/api/models"

interface TDGProps
{
  formDesc: FormDescription
}

const TheDataGrid = ({formDesc}: TDGProps) =>
{
  const [entryData, setEntryData] = useState<FormAnswers[]>([])

  useEffect(() => {

  })

  return <>
    TO DO
  </>
}

export default TheDataGrid
