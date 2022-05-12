import { useEffect, useMemo, useState } from "react"
import API from "~/api"
import { FormAnswers, FormDescription } from "~/api/models"

import { AgGridReact } from '@ag-grid-community/react';
import { ClientSideRowModelModule } from '@ag-grid-community/client-side-row-model';
import { RangeSelectionModule } from '@ag-grid-enterprise/range-selection';
import { RowGroupingModule } from '@ag-grid-enterprise/row-grouping';
import { RichSelectModule } from '@ag-grid-enterprise/rich-select';

import { ColDef, ModuleRegistry } from '@ag-grid-community/core';

import 'ag-grid-enterprise'
import '@ag-grid-community/core/dist/styles/ag-grid.css';
import '@ag-grid-community/core/dist/styles/ag-theme-alpine-dark.css';
import '@ag-grid-community/core/dist/styles/ag-theme-balham.css';
import '@ag-grid-community/core/dist/styles/ag-theme-balham-dark.css';
import '@ag-grid-community/core/dist/styles/ag-theme-material.css';
import { Box } from "@mui/material";

ModuleRegistry.registerModules([ClientSideRowModelModule, RangeSelectionModule, RowGroupingModule, RichSelectModule]);

interface TDGProps
{
  formDesc: FormDescription
}

const TheDataGrid = ({formDesc}: TDGProps) =>
{
  console.log(formDesc.authorEmail)
  console.log("Rendering the grid")

  const [entryData, setEntryData] = useState<{[x: string]: string}[]>([])

  console.log(entryData)

  useEffect(() => {
    const getter = async () => {
      const data = await API.Entry.ViewFormEntries({
        count: 100000,
        offset: 0,
        formId: formDesc.formId})
      console.log(data)
      const transformed = data.entries.map(fa => {
        const entry: any = {}
        fa.answers.map((x, i) => {
          entry[formDesc.questions[i].title] = x
        })
        console.log("Entries")
        console.log(entry)
        return entry
      })

      console.log("Date:")
      console.log(transformed)
      setEntryData(transformed)
    }

    getter()
  }, [])

  const columnDefs: ColDef[] = useMemo(() => formDesc.questions.map(
    q => ({field: q.title}))
  , [formDesc.questions]);
  columnDefs[0] = {...columnDefs[0], headerCheckboxSelection: true,
    headerCheckboxSelectionFilteredOnly: true, checkboxSelection: true}

  console.log("Columns:")
  console.log(columnDefs)

  // never changes, so we can use useMemo
  const defaultColDef = useMemo(() => ({
    resizable: true,
    sortable: true
  }), []);

  return <Box className="ag-theme-alpine-dark" style={{height: "calc(100vh - 300px)"}}>
    <AgGridReact
        // className="ag-theme-alpine"
        animateRows={true}
        columnDefs={columnDefs}
        defaultColDef={defaultColDef}
        enableRangeSelection={true}
        rowData={entryData}
        rowSelection="multiple"
        suppressRowClickSelection={true}
    />
  </Box>
}

export default TheDataGrid
