import { Button, FormControl, FormHelperText, Input, InputLabel } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { Form } from '~/api/form';
import { FormList } from '~/api/form/list';

export default function SubmitForm(): JSX.Element
{
  const [nrDocs, setNrDocs] = useState(0);
  const [files, setFiles] = useState(undefined)

  const GetForms = async () => {
    const data = await FormList({count: 1000, offset: 0})
    console.log("Received data:");
    console.log(data);
    setNrDocs(data.forms.length);
  }

  const doUpload = async (file: Blob) => {
    console.log("Querying the god damn inferencee")
    let formData = new FormData();
    formData.append("file", file);
    const answers = await Form.Submit(formData);
    console.log(answers)
  }

  const selectFile = (e: any) => {
    setFiles(e.target.file)
  }

  const sendButton = () => {
    doUpload(files as unknown as Blob)
  }

  return <>
    <FormControl>
      {/* <InputLabel htmlFor="my-file">Image/PDF/ZIP</InputLabel> */}
      <Input id="my-file" type="file" />
      <FormHelperText id="my-helper-text">We'll never share your email.</FormHelperText>
    </FormControl>
    <Button onClick={sendButton}>Send</Button>
  </>
}
