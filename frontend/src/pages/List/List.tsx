import React, { useEffect, useState } from 'react';
import API from '~/api';
import { FormDescription } from '~/api/models';
import CustomFormsDrawer from './CustomFormsDrawer';

export default function List(): JSX.Element
{
  const [forms, setForms] = useState<FormDescription[]>([])

  const GetForms = async () => {
    const data = await API.Form.FormList({count: 10000, offset: 0})
    console.log("Received data:");
    console.log(data);
    setForms(data.forms)
  }

  useEffect(() => {
    GetForms()
  }, [])

  return <>
    <CustomFormsDrawer forms={forms} title={'some forms'}/>
  </>
}
