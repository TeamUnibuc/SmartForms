import React from 'react'

import Grid from '@mui/material/Grid';
import EditFormPdfDisplay from './EditFormPdfDisplay';

import GenerateButton from '~/components/EditForm/GenerateButton';
import DynamicQuestionList from '~/components/EditForm/DynamicQuestionList';
import { QLContextProvider } from '~/contexts/QLContext';
import CreateFormButton from '~/components/EditForm/CreateFormButton';
import { Divider } from '@mui/material';
import EditFormInfo from './EditFormInfo';
import { useUserState } from '~/contexts/UserContext';
import SimpleMessage from '~/components/SimpleMessage';

export default function EditForm(): JSX.Element
{
  const {authenticated} = useUserState()

  const disabled = !authenticated

  return <>
    <QLContextProvider>
      <Grid container columnSpacing={1}>
          <Grid item xs={4}>
              <EditFormInfo />
              <DynamicQuestionList />
          </Grid>

          <Grid item xs={2}>
            {disabled ?
              <SimpleMessage color='warning' msg='You need to be logged in'/>
            : <>
              <GenerateButton disabled={disabled}/>
              <CreateFormButton disabled={disabled}/>
            </>
            }
          </Grid>

          <Grid item xs={6}>
            <EditFormPdfDisplay />
          </Grid>
      </Grid>
    </QLContextProvider>
  </>
}
