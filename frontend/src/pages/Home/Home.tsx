import React from 'react'

import { Button } from '@material-ui/core'

export default function Home(): JSX.Element
{
  return <>
    <p>Hello, this is the home page</p>
    <Button variant="contained" href="/edit-form">Edit Form</Button>
  </>
}
