import { Box } from '@mui/material';
import React, { useEffect, useState } from 'react';
import API from '~/api';
import { FormDescription } from '~/api/models';
import CustomFormsDrawer from './CustomFormsDrawer';

export default function List(): JSX.Element
{
  console.log("Render main List comp")
  const [forms, setForms] = useState<FormDescription[]>([])

  const GetForms = async () => {
    const data = await API.Form.FormList({count: 10000, offset: 0, isOwner: true})
    console.log("Received data:");
    console.log(data);
    setForms(data.forms)
  }

  useEffect(() => {
    GetForms()
  }, [])

  return <Box width='100%'>
    <CustomFormsDrawer forms={forms} title={'MY FORMS'} openDelay=
    {700}/>

    <CustomFormsDrawer forms={forms} title={'OTHER FORMS'}/>
  </Box>
}
