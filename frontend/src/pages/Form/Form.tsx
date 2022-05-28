import { Box, Alert, Typography, Tabs, Tab, useTheme, Button, Snackbar, AlertColor } from "@mui/material"
import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import SwipeableViews from 'react-swipeable-views';
import API from "~/api"
import { FormDescription } from "~/api/models"
import { GridExample } from "./AgGrid";
// import TheDataGrid from "./TheDataGrid";

// import {  } from "@ag-grid-community/core/dist/styles"

// import 'ag-grid-community/dist/styles/ag-grid.css'; // Core grid CSS, always needed
// import 'ag-grid-community/dist/styles/ag-theme-alpine.css'; // Optional theme CSS
import PdfDisplay from "~/components/PdfDisplay";
import NonEditableAnswers from "~/components/NonEditableAnswers";
import { useUserState } from "~/contexts/UserContext";


import Settings from "./Settings";
import TheDataGrid from "./TheDataGrid";

// Code inspired from https://mui.com/material-ui/react-tabs/#full-width

const FormPage = () =>
{

  const [searchParams, _setSearchParams] = useSearchParams()
  const [formData, setFormData] = useState<undefined | FormDescription>()
  const [loading, setLoading] = useState(true)
  const [value, setValue] = useState(0);
  const [pdfString, setPdfString] = useState("")
  const userState = useUserState()
  const theme = useTheme();

  const [snackOpen, setSnackOpen] = useState(false)
  const [snackState, setSnackState] = useState({msg: "", sev: "info"})

  const formOwner = userState.data?.email === formData?.authorEmail
  const formId = searchParams.get("formId")

  useEffect(() => {
    (() => {
      if (formData === undefined) {
        API.Form.Description(formId || "idiot")
          .then(async r => {
            setFormData(r)
            const previewData = await API.Form.Pdf(r.formId)
            setPdfString(previewData.formPdfBase64)
          })
          .catch(e => console.log(`Error getting formId: ${e}`))
          .finally(() => setLoading(false))
      }
    })()
  }, [formData])

  if (loading)
    return <Alert severity="info"><Typography>Loading ...</Typography></Alert>

  if (formData === undefined)
    return <Alert severity={"error"}> Could not find form :/ </Alert>

  const a11yProps = (index: number) => {
    return {
      id: `full-width-tab-${index}`,
      'aria-controls': `full-width-tabpanel-${index}`,
    };
  }

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const handleChangeIndex = (index: number) => {
    setValue(index);
  };

  const handleSnackClose = (event: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackOpen(false);
  };

  const tabElements = [
    {tab: "Data",
     content: <TheDataGrid formDesc={formData}/>
    //  content: <GridExample />
    },
    {tab: "Questions",
     content: <NonEditableAnswers questions={formData.questions}/>},
    {tab: "Form",
     content: <PdfDisplay pdfString={pdfString}/>},
    {tab: "Settings",
     content: <Settings
      formId={formData.formId}
      snack={[setSnackOpen, setSnackState]}
      formData={formData}
    />}
  ]

  const chosenEl = formOwner ? [0, 1, 2, 3] : [1, 2]

  console.log(`Owner: ${formOwner}`)
  return <Box id="form-page" width='100%' height='100%'
    style={{
      display: 'flex',
      flexFlow: 'column'
    }}
  >

  <Tabs
    value={value}
    onChange={handleChange}
    indicatorColor="secondary"
    textColor="inherit"
    variant="fullWidth"
    aria-label="full width tabs example"
  >
    {chosenEl.map((id, index) =>
      <Tab key={index} label={tabElements[id].tab}/>
    )}
  </Tabs>

  <SwipeableViews id="swipeable-views"
    style={{flexGrow: '1', height: '100%'}}
    axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
    index={value}
    onChangeIndex={handleChangeIndex}
  >
    {chosenEl.map((id, index) =>
      <TabPanel key={index} value={value} index={index} dir={theme.direction}>
        {tabElements[id].content}
      </TabPanel>
    )}
  </SwipeableViews>

  <Snackbar
    anchorOrigin={{vertical: 'bottom', horizontal: 'center'}}
    open={snackOpen}
    autoHideDuration={5000}
    onClose={handleSnackClose}
  >
    <Alert
      onClose={handleSnackClose}
      severity={snackState.sev as AlertColor}
      sx={{ width: '100%' }}
    >
      {snackState.msg}
    </Alert>
  </Snackbar>

  </Box>
}

interface TabPanelProps {
  children?: React.ReactNode;
  dir?: string;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      style={{height: '100%'}}
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box height='100%'>
          {children}
        </Box>
      )}
    </div>
  );
}

export default FormPage
