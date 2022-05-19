import React from 'react'

import Grid from '@mui/material/Grid';
import EditFormPdfDisplay from './EditFormPdfDisplay';

import GenerateButton from '~/components/EditForm/GenerateButton';
import DynamicQuestionList from '~/components/EditForm/DynamicQuestionList';
import { QLContextProvider } from '~/contexts/CoolContext';
import CreateFormButton from '~/components/EditForm/CreateFormButton';
import { Divider } from '@mui/material';
import EditFormInfo from './EditFormInfo';

export default function EditForm(): JSX.Element
{
  return <>
    <QLContextProvider>
      <Grid container columnSpacing={1}>
          <Grid item xs={4}>
              <EditFormInfo />
              <DynamicQuestionList />
          </Grid>

          <Grid item xs={2}>
            <GenerateButton />
            <CreateFormButton />
          </Grid>

          <Grid item xs={6}>
            <EditFormPdfDisplay />
          </Grid>
      </Grid>
    </QLContextProvider>
  </>
}
