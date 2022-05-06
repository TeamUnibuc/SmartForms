import { useEffect, useState } from "react"
import API from "~/api"
import { FormAnswers, FormDescription } from "~/api/models"

interface TDGProps
{
  formDesc: FormDescription
}

const TheDataGrid = ({formDesc}: TDGProps) =>
{
  console.log("Rendering the grid")

  const [entryData, setEntryData] = useState<FormAnswers[]>([])

  useEffect(() => {
    const getter = async () => {
      const data = await API.Entry.ViewFormEntries({
        count: 100000,
        offset: 0,
        formId: formDesc.formId})
      setEntryData(data.entries)
      console.log(data.entries)
    }

    getter()
  })

  return <>
    TO DO
  </>
}

export default TheDataGrid
