import React from 'react';

import { Routes, Route, BrowserRouter as Router } from 'react-router-dom'
import { Box, Container, Grid } from '@mui/material';

import Footer from '~/components/General/Footer';
import Header from '~/components/General/Header';
import { Home, EditForm, List, SubmitForm, FormPage } from '~/pages'
import { UserContextProvider } from '~/contexts/UserContext';

import './App.css'
import FastSubmit from './pages/FastSubmit/FastSubmit';

interface AppProps
{
  themeChanger: React.Dispatch<React.SetStateAction<boolean>>
  isDarkTheme: boolean
}

function App(props: AppProps): JSX.Element {
  if (import.meta.env.DEV) {
    console.log("Printing all env variables")
    console.log(import.meta.env)
  }

  return (
  <UserContextProvider >
    <Router basename={import.meta.env.BASE_URL}>
      <Box style={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        // // alignItems: 'center',
        // // flexGrow: 1,
        // width: '100%',
      }}>

      <Box >
        <Header {...props} />
      </Box>

      <Box style={{height: '100%'}}>

        <Container style={{
          height: '100%'
        }}>

          <Routes>
              <Route key="Home" path="/"
                      element={<Home />}/>
              <Route key="EditForm" path="/edit-form"
                      element={<EditForm />} />
              <Route key="List" path="/list"
                      element={<List />} />
              <Route key="Submit" path="/submit-form"
                      element={<SubmitForm />}/>
              <Route key="Form" path="/form"
                      element={<FormPage />}/>
              <Route key="FastSubmit" path="/fast-submit"
                      element={<FastSubmit />}/>
          </Routes>

          <Footer />
        </Container>
      </Box>

      </Box>
    </Router>
  </UserContextProvider>
  );
}

export default App;
