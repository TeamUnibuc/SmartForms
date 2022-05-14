import { Box, Alert, Typography, Tabs, Tab, useTheme, Button } from "@mui/material"
import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import SwipeableViews from 'react-swipeable-views';
import API from "~/api"
import { FormDescription } from "~/api/models"
import MyAgGrid from "./AgGrid";
import TheDataGrid from "./TheDataGrid";

import 'ag-grid-community/dist/styles/ag-grid.css'; // Core grid CSS, always needed
import 'ag-grid-community/dist/styles/ag-theme-alpine.css'; // Optional theme CSS
import PdfDisplay from "~/components/PdfDisplay";
import NonEditableAnswers from "~/components/NonEditableAnswers";
import { useUserState, useUserUpdater } from "~/contexts/UserContext";

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

  console.log(`Owner: ${formOwner}`)
  return <Box width='100%'>


  <Tabs
    value={value}
    onChange={handleChange}
    indicatorColor="secondary"
    textColor="inherit"
    variant="fullWidth"
    aria-label="full width tabs example"
  >
    <Tab label="Data" {...a11yProps(0)} />
    <Tab label="Questions" {...a11yProps(1)} />
    <Tab label="Form" {...a11yProps(2)} />
  </Tabs>

  <SwipeableViews
    axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
    index={value}
    onChangeIndex={handleChangeIndex}
  >
    <TabPanel value={value} index={0} dir={theme.direction}>
      <TheDataGrid formDesc={formData}/>
    </TabPanel>
    <TabPanel value={value} index={1} dir={theme.direction}>
      <NonEditableAnswers questions={formData.questions}/>
    </TabPanel>
    <TabPanel value={value} index={2} dir={theme.direction}>
      <PdfDisplay pdfString={pdfString}/>
    </TabPanel>
  </SwipeableViews>

  {formOwner &&
  <Box>
    <Typography color="#a1c9c5" variant="h6" sx={{mb: 2}} style={{fontWeight: 500}}>
      Form Commands:
    </Typography>
    <Button color="error" variant="contained">
      Delete
    </Button>
  </Box>
  }

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
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default FormPage
