import { Button, Divider, FormControl, FormHelperText, Input, List, ListItem, ListItemIcon, ListItemText, Typography } from "@mui/material"
import { Dispatch, ReactNode, SetStateAction, useState } from "react"
import API from "~/api"
import { InferenceResponse } from "~/api/inference/infer"

import FolderIcon from '@mui/icons-material/Folder';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import UploadIcon from '@mui/icons-material/Upload';

interface SubmitCompProps {
  setInferenceDone: Dispatch<SetStateAction<boolean>>
  setAnswers: Dispatch<SetStateAction<InferenceResponse>>
}

const SubmitComp = (props: SubmitCompProps) =>
{
  const [additionalText, setAdditionalText] = useState("")
  const [files, setFiles] = useState<FileList | undefined>()
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
    if (files.length == 1)
      setAdditionalText(`Uploaded 1 file: ${files[0].name}`)
    else
      setAdditionalText(`Uploaded ${files.length} files`)
    setFiles(files)
  }

  const sendButton = () => {
    doUpload(files as FileList)
  }

  return <>
  <FormControl variant="filled">

    <input
      // className={classes.input}
      style={{ display: 'none' }}
      id="my-file" type="file" name='fileUploads'
      multiple
      onChange={selectFile}
    />
    <label htmlFor="my-file">
      <Button variant="contained" component="span" sx={{mb: 2}}>
        <UploadIcon />
        Upload
      </Button>
    </label>

  </FormControl>

  {files &&
    <List>
    {Array.from(files).map((f, i) =>
      <ListItem key={i}>
        <ListItemIcon>
          <InsertDriveFileIcon />
        </ListItemIcon>
        <ListItemText
          primary={f.name}
        />
      </ListItem>
    )}
    </List>
  }

  <Divider sx={{mt: 2}}/>
  <Button
      sx={{mt: 5}}
      onClick={sendButton}
      variant="contained"
      color="success"
      disabled={files === undefined}>
    Send
  </Button>
  </>
}

export default SubmitComp
