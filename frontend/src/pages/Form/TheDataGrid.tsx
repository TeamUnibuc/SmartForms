import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import API from "~/api"
import { FormAnswers, FormDescription } from "~/api/models"

import { AgGridReact } from '@ag-grid-community/react';
import { ClientSideRowModelModule } from '@ag-grid-community/client-side-row-model';
import { RowGroupingModule } from '@ag-grid-enterprise/row-grouping';
import { RichSelectModule } from '@ag-grid-enterprise/rich-select';
import { GridChartsModule } from '@ag-grid-enterprise/charts';
import { ClipboardModule } from '@ag-grid-enterprise/clipboard';
import { ExcelExportModule } from '@ag-grid-enterprise/excel-export';
import { CsvExportModule } from '@ag-grid-community/csv-export';
import { MenuModule } from '@ag-grid-enterprise/menu';
import { RangeSelectionModule } from '@ag-grid-enterprise/range-selection';


import { ColDef, ModuleRegistry } from '@ag-grid-community/core';

// import 'ag-grid-enterprise'
import '@ag-grid-community/core/dist/styles/ag-grid.css';
import '@ag-grid-community/core/dist/styles/ag-theme-alpine-dark.css';
import '@ag-grid-community/core/dist/styles/ag-theme-alpine.css';
import '@ag-grid-community/core/dist/styles/ag-theme-balham.css';
import '@ag-grid-community/core/dist/styles/ag-theme-balham-dark.css';
import '@ag-grid-community/core/dist/styles/ag-theme-material.css';
import { Box, Button } from "@mui/material";
import isDarkTheme from "~/utils/themeGetter";

ModuleRegistry.registerModules([
  ClientSideRowModelModule,
  CsvExportModule,
  ExcelExportModule,
  MenuModule

  // ClientSideRowModelModule,
  // RangeSelectionModule,
  // RowGroupingModule,
  // RichSelectModule,
  // ClipboardModule,
  // GridChartsModule,
  // MenuModule,
  // ExcelExportModule,
  // RangeSelectionModule,
]);

interface TDGProps
{
  formDesc: FormDescription
}

const TheDataGrid = ({formDesc}: TDGProps) =>
{
  const gridRef = useRef<AgGridReact>(null);

  const [entryData, setEntryData] = useState<{[x: string]: string}[]>([])

  const popupParent = useMemo<HTMLElement>(() => {
    const el = document.querySelector('body')
    console.log(el)
    return el  as HTMLElement;
  }, []);



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
        return entry
      })

      setEntryData(transformed)
    }

    getter()
  }, [])

  const columnDefs: ColDef[] = useMemo(() => formDesc.questions.map(
    q => ({field: q.title}))
  , [formDesc.questions]);
  columnDefs[0] = {...columnDefs[0], headerCheckboxSelection: true,
    headerCheckboxSelectionFilteredOnly: true, checkboxSelection: true}

  // never changes, so we can use useMemo
  const defaultColDef = useMemo(() => ({
    resizable: true,
    sortable: true
  }), []);

  const themeClass = `ag-theme-alpine${isDarkTheme() ? '-dark' : ''}`

  const onBtnExport = useCallback(() => {
    gridRef.current!.api.exportDataAsCsv();
  }, []);

  const onBtnExcel = useCallback(() => {
    gridRef.current!.api.exportDataAsExcel();
  }, [])

  return <>
    <Box display="flex">
      <Button
        onClick={onBtnExport}
        sx={{m: 1}}
        variant="contained"
      >
        Download CSV export file
      </Button>

      <Button
          onClick={onBtnExcel}
          sx={{m: 1}}
          variant="contained"
      >
        Download XLSX export file
      </Button>

    </Box>

    <Box className={themeClass} style={{height: "calc(80vh)"}}>
      <AgGridReact
          // className="ag-theme-alpine"
          ref={gridRef}
          rowData={entryData}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          // animateRows={true}
          // enableRangeSelection={true}
          // rowSelection="multiple"
          // suppressRowClickSelection={true}
          // popupParent={popupParent}
      />

    </Box>
  </>

}

export default TheDataGrid
