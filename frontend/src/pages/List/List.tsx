import React, { useEffect, useState } from 'react';
import { FormList } from '~/api/form/list';

export default function List(): JSX.Element
{
  const [nrDocs, setNrDocs] = useState(0);

  const GetForms = async () => {
    const data = await FormList({count: 1000, offset: 0})
    console.log("Received data:");
    console.log(data);
    setNrDocs(data.forms.length);
  }

  useEffect(() => {
    GetForms()
  }, [])

  return <>
    <p>Number of total documents: {setNrDocs}</p>
  </>
}
