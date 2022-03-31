import React, { ChangeEvent, SyntheticEvent, useContext, useState } from 'react'

import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import PdfDisplay from './PdfDisplay';

import { FormPreview } from '~/api/form/preview'
import TextField from '@mui/material/TextField';
import TextQuestion from '~/components/TextQuestion';
import { QuestionList, QuestionListConsumer, QuestionListProvider } from '~/contexts/QuestionList';
import GenerateButton from '~/components/GenerateButton';

export default function EditForm(): JSX.Element
{
  // const gen_updater = (q_ind: number) =>
  // {
  //   const form_data_updater = (q: Question) => {
  //     let new_data = formData
  //     new_data[q_ind] = q
  //     setFormData(new_data)
  //   }

  //   return form_data_updater
  // }

  return <>
    <QuestionListProvider>
      <Grid container columnSpacing={1}>
        <Grid item xs={4}>
          <TextQuestion q_ind={1}/>
          <TextQuestion q_ind={2}/>
        </Grid>

        <Grid item xs={2}>
          <GenerateButton />
        </Grid>

        <Grid item xs={6}>
          <PdfDisplay />
        </Grid>
      </Grid>
    </QuestionListProvider>
  </>
}
