import { AgGridReact } from "ag-grid-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { FormDescription } from "~/api/models"


import 'ag-grid-enterprise'

import 'ag-grid-community/dist/styles/ag-grid.css'; // Core grid CSS, always needed
// import 'ag-grid-community/dist/styles/ag-theme-alpine.css'; // Optional theme CSS
import 'ag-grid-community/dist/styles/ag-theme-material.css'; // Optional theme CSS
// import 'ag-grid-community/dist/styles/ag-theme-classic.css'; // Optional theme CSS
// import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css'; // Optional theme CSS
import { Box } from "@mui/material";

interface TDGProps
{
  formDesc: FormDescription
}

const MyAgGrid = ({formDesc}: TDGProps) =>
{
  // const gridRef = useRef(); // Optional - for accessing Grid's API
 const [rowData, setRowData] = useState(); // Set rowData to Array of Objects, one Object per Row

 // Each Column Definition results in one Column.
 const [columnDefs, setColumnDefs] = useState([
   {field: 'make', filter: true},
   {field: 'model', filter: true, headerCheckboxSelection: true,
   headerCheckboxSelectionFilteredOnly: true,
   checkboxSelection: true},
   {field: 'price'}
 ]);

 // DefaultColDef sets props common to all Columns
 const defaultColDef = useMemo( ()=> ({
    sortable: true,
    resizable: true
  }), []);

 // Example of consuming Grid Event
 const cellClickedListener = useCallback( event => {
   console.log('cellClicked', event);
 }, []);

 // Example load data from sever
 useEffect(() => {
   fetch('https://www.ag-grid.com/example-assets/row-data.json')
   .then(result => result.json())
   .then(rowData => setRowData(rowData))
 }, []);

 // Example using Grid's API
 const buttonListener = useCallback( e => {
  // if (!gridRef) return
  // gridRef.current.api.deselectAll();
 }, []);

 return (
   <div>

     {/* Example using Grid's API */}
     <button onClick={buttonListener}>Push Me</button>

     {/* On div wrapping Grid a) specify theme CSS Class Class and b) sets Grid size */}
     <Box className="ag-theme-material" style={{height: "calc(100vh - 300px)"}}>

       <AgGridReact
          //  ref={gridRef} // Ref for accessing Grid's API

          rowData={rowData} // Row Data for Rows

          enableRangeSelection={true}

          columnDefs={columnDefs} // Column Defs for Columns
          defaultColDef={defaultColDef} // Default Column Properties

          animateRows={true} // Optional - set to 'true' to have rows animate when sorted
          rowSelection='multiple' // Options - allows click selection of rows
          onCellClicked={cellClickedListener} // Optional - registering for Grid Event
           />
     </Box>
   </div>
 )
}

export default MyAgGrid
