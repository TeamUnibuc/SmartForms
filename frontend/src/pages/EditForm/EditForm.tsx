import React from 'react'

import Grid from '@mui/material/Grid';
import PdfDisplay from './PdfDisplay';

import { QuestionListProvider } from '~/contexts/QuestionList';
import GenerateButton from '~/components/GenerateButton';
import DynamicQuestionList from '~/components/DynamicQuestionList';
import { QLContextProvider } from '~/contexts/CoolContext';

export default function EditForm(): JSX.Element
{
  return <>
    <QuestionListProvider>
      <Grid container columnSpacing={1}>
        <QLContextProvider>
          <Grid item xs={4}>
              <DynamicQuestionList />
          </Grid>

          <Grid item xs={2}>
            <GenerateButton />
          </Grid>

          <Grid item xs={6}>
            <PdfDisplay />
          </Grid>
        </QLContextProvider>
      </Grid>
    </QuestionListProvider>
  </>
}
