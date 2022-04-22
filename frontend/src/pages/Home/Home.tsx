import { Button } from '@mui/material'
import React from 'react'

export default function Home(): JSX.Element
{
  return <>
    <p>Hello, this is the home page</p>
    <Button variant="contained" href="/edit-form">Edit Form</Button>
  </>
}
