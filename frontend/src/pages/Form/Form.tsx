import { Box, Alert, Typography, Tabs, Tab, useTheme } from "@mui/material"
import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import SwipeableViews from 'react-swipeable-views';
import API from "~/api"
import { FormDescription } from "~/api/models"
import TheDataGrid from "./TheDataGrid";

// Code inspired from https://mui.com/material-ui/react-tabs/#full-width

const FormPage = () =>
{
  const [searchParams, _setSearchParams] = useSearchParams()
  const [formData, setFormData] = useState<undefined | FormDescription>()
  const [loading, setLoading] = useState(true)
  const [value, setValue] = useState(0);
  const theme = useTheme();

  const formId = searchParams.get("formId")

  useEffect(() => {
    const getter = async () => {
      await API.Form.Description(formId || "idiot")
        .then(r => setFormData(r))
        .catch(e => console.log(`Error getting formId: ${e}`))
        .finally(() => setLoading(false))
    }

    getter()
  }, [])

  if (loading)
    return <Alert severity="info"><Typography>Loading ...</Typography></Alert>

  if (formData === undefined)
    return <Alert severity={"error"}> Could not find form :/ </Alert>

  console.log(formData)

  const a11yProps = (index: number) => {
    return {
      id: `full-width-tab-${index}`,
      'aria-controls': `full-width-tabpanel-${index}`,
    };
  }

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const handleChangeIndex = (index: number) => {
    setValue(index);
  };

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
      Item Two
    </TabPanel>
  </SwipeableViews>

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