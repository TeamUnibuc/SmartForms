import React from 'react'

import Grid from '@mui/material/Grid';
import PdfDisplay from './PdfDisplay';

import GenerateButton from '~/components/EditForm/GenerateButton';
import DynamicQuestionList from '~/components/EditForm/DynamicQuestionList';
import { QLContextProvider } from '~/contexts/CoolContext';
import CreateFormButton from '~/components/EditForm/CreateFormButton';
import { Divider } from '@mui/material';

export default function EditForm(): JSX.Element
{
  return <>
    <QLContextProvider>
      <Grid container columnSpacing={1}>
          <Grid item xs={4}>
              <DynamicQuestionList />
          </Grid>

          <Grid item xs={2}>
            <GenerateButton />
            <CreateFormButton />
          </Grid>

          <Grid item xs={6}>
            <PdfDisplay />
          </Grid>
      </Grid>
    </QLContextProvider>
  </>
}
