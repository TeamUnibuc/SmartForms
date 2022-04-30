import { Button, Divider, FormControl, FormHelperText, Input } from "@mui/material"
import { Dispatch, SetStateAction, useState } from "react"
import API from "~/api"
import { InferenceResponse } from "~/api/inference/infer"


interface SubmitCompProps {
  setInferenceDone: Dispatch<SetStateAction<boolean>>
  setAnswers: Dispatch<SetStateAction<InferenceResponse>>
}

const SubmitComp = (props: SubmitCompProps) =>
{
  const [files, setFiles] = useState<unknown>(undefined)
  const {setInferenceDone, setAnswers} = props

  const doUpload = async (files: FileList) => {
    console.log("Querying the god damn inferencee")
    let formData = new FormData();
    for (const file of files) {
      formData.append(`fileUploads`, file, file.name)
    }
    const answers = await API.Inference.Infer(formData)
    setInferenceDone(true)
    setAnswers(answers)
  }

  const selectFile = (e: any) => {
    const files = e.target.files as FileList
    setFiles(files)
  }

  const sendButton = () => {
    doUpload(files as FileList)
  }

  return <>
  <FormControl variant="filled">
    <Input id="my-file" type="file" name='fileUploads'
      onChange={selectFile}
      inputProps={{
        multiple: true
      }}/>

    <FormHelperText id="my-helper-text">
        Placeholder text
      </FormHelperText>

  </FormControl>
  <Divider />
  <Button onClick={sendButton} variant="contained">
    Send
  </Button>
  </>
}

export default SubmitComp
