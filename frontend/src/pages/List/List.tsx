import { Box } from '@mui/material';
import React, { useEffect, useState } from 'react';
import API from '~/api';
import { FormDescription } from '~/api/models';
import { useUserState } from '~/contexts/UserContext';
import CustomFormsDrawer from './CustomFormsDrawer';

export default function List(): JSX.Element
{
  console.log("Render main List comp")

  const {authenticated, data: userDetails} = useUserState()

  const [formsOwned, setFormsOwned] = useState<FormDescription[]>([])
  const [formsAll, setFormsAll] = useState<FormDescription[]>([])

  console.log(`Authenticated from List: ${authenticated}`)

  const GetForms = async () => {
    if (authenticated === undefined)
      return
    let dataOwned = undefined
    if (authenticated) {
      dataOwned = await API.Form.FormList({
        count: 10000, offset: 0, isOwner: true})
      setFormsOwned(dataOwned.forms)
      console.log("Authenticated list forms")
      console.log(dataOwned)
    }

    const dataAll = await API.Form.FormList({
        count: 10000, offset: 0, isOwner: false})

    setFormsAll(dataAll.forms.filter(f => f.authorEmail !== userDetails?.email))
  }

  useEffect(() => {
    GetForms()
  }, [authenticated])

  return <Box width='100%'>
    {authenticated ?
      <CustomFormsDrawer forms={formsOwned} title={'MY FORMS'}/>
    :
      <></>
    }

    <CustomFormsDrawer forms={formsAll} title={'OTHER FORMS'}/>

  </Box>
}
