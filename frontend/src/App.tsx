import React from 'react';

import { Box, Container, createTheme, CssBaseline, Grid, ThemeOptions } from '@mui/material';
import { StylesProvider, ThemeProvider } from '@mui/styles';
import { Routes, Route, BrowserRouter as Router } from 'react-router-dom'

import Footer from '~/components/Footer';
import Header from '~/components/Header';
import { Home, EditForm, List } from '~/pages'

export const themeOptions: ThemeOptions = {
  palette: {
    mode: 'dark',
    primary: {
      main: '#5893df',
    },
    secondary: {
      main: '#2ec5d3',
    },
    background: {
      default: '#192231',
      paper: '#24344d',
    },
  },
};

// Daca vrem sa adaugam culori la theme, aici trebuie sa facem asta
const darkTheme = createTheme(themeOptions);


function App(): JSX.Element {
  if (import.meta.env.DEV) {
    console.log("Printing all env variables")
    console.log(import.meta.env)
  }

  return (
    // <StylesProvider injectFirst>
    <>
        <Router basename={import.meta.env.BASE_URL}>
        {/* <SnackProvider> */}
        {/* <UserStatusProvider> */}
      <ThemeProvider theme={darkTheme}>

          {/* <Snackbar /> */}

          <Grid container>

            <Grid item xs={12}>
              <Header />
            </Grid>

            <Grid item xs={12}>
              <Box pt={2} paddingBottom="100px">
                <Container style={{display: 'flex', flexDirection: 'column', alignItems: 'center', flexGrow: 1, width: '100%'}}>

                  <Routes>
                    <Route key="Home" path="/" element={<Home />}/>
                    <Route key="EditForm" path="/edit-form" element={<EditForm />} />
                    <Route key="List" path="/list" element={<List />} />
                  </Routes>

                  <Footer />
                </Container>

              </Box>
            </Grid>

          </Grid>

      </ThemeProvider>
        {/* </UserStatusProvider> */}
        {/* </SnackProvider> */}
        </Router>
    </>
    // </StylesProvider>
  );
}

export default App;
