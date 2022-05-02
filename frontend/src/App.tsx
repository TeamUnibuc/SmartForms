import React from 'react';

import { Routes, Route, BrowserRouter as Router } from 'react-router-dom'
import { Container, Grid } from '@mui/material';

import Footer from '~/components/General/Footer';
import Header from '~/components/General/Header';
import { Home, EditForm, List, SubmitForm } from '~/pages'
import { UserContextProvider } from '~/contexts/UserContext';

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
  <UserContextProvider>
    <Router basename={import.meta.env.BASE_URL}>
      <Grid container>

      <Grid item xs={12}>
        <Header {...props} />
      </Grid>

      <Grid item xs={12}>

        <Container style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          flexGrow: 1,
          width: '100%',
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
        </Routes>

          <Footer />
        </Container>
      </Grid>

      </Grid>
    </Router>
  </UserContextProvider>
  );
}

export default App;
