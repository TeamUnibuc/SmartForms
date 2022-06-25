import React, { useEffect, useState } from 'react'

import { Box, Button, Divider, Typography } from '@mui/material'
import API from '~/api'

export default function Home(): JSX.Element
{
  const [forms, setForms] = useState<number | undefined>()
  const [entries, setEntries] = useState<number | undefined>()

  useEffect(() => {
    (async () => {
      const data = await API.Statistics.StatsGlobal()
      setForms(data.total_number_of_forms)
      setEntries(data.total_number_of_entries)
    })()
  }, [])

  return <>
    <Typography variant="h6" sx={{mb: 1}} style={{fontWeight: 500}}>
      Proudly hosting <span style={{color: "#a1c9c5"}}>{forms}</span> forms
    </Typography>
    <Typography variant="h6" sx={{mb: 2}} style={{fontWeight: 500}}>
      With over <span style={{color: "#a1c9c5"}}>{entries}</span> entries!
    </Typography>

    <Divider />

    <Box display="flex" style={{alignItems: "center", flexFlow: "column"}} sx={{mb: 1}}>
      <Typography sx = {{m: 2}}>
        Start creating a form right now!
      </Typography>

      <Button variant="contained" href="/edit-form">
        Create New Form
      </Button>

    </Box>
  </>
}
