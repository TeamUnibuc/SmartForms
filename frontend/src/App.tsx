import React from 'react';
import { StylesProvider } from '@material-ui/styles';
import { Routes, Route, BrowserRouter as Router } from 'react-router-dom'

import Footer from '~/components/Footer';
import Header from '~/components/Header';
import { Home, EditForm } from '~/pages'

import { Grid, Box, Container, CssBaseline } from '@material-ui/core'
import { ThemeProvider } from '@material-ui/styles'
import { createTheme } from '@material-ui/core/styles';

// Daca vrem sa adaugam culori la theme, aici trebuie sa facem asta
const theme = createTheme({
  palette: {
    background:{
      default: '#CDDDDD'
    }
  }
})

function App(): JSX.Element {
  if (import.meta.env.DEV) {
    console.log("Printing all env variables")
    console.log(import.meta.env)
  }

  return (
    <StylesProvider injectFirst>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router basename={import.meta.env.BASE_URL}>
        {/* <SnackProvider> */}
        {/* <UserStatusProvider> */}

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
                  </Routes>

                  <Footer />
                </Container>

              </Box>
            </Grid>

          </Grid>

        {/* </UserStatusProvider> */}
        {/* </SnackProvider> */}
        </Router>
      </ThemeProvider>
    </StylesProvider>
  );
}

export default App;
