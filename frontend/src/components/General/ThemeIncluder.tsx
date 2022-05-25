import { createTheme, CssBaseline, StyledEngineProvider, ThemeOptions, ThemeProvider } from "@mui/material";
import React, { useState } from "react"
import App from "~/App";
import isDarkTheme from "~/utils/themeGetter";

const DarkThemeOptions: ThemeOptions = {
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

const LightThemeOptions: ThemeOptions = {
  palette: {
    mode: 'light'
  }
}

const DarkTheme = createTheme(DarkThemeOptions)
const LightTheme = createTheme(LightThemeOptions)

const ThemeIncluder: React.FC = (props) =>
{
  const [issDarkTheme, setIsDarkTheme] = useState(isDarkTheme())

  return <ThemeProvider theme={issDarkTheme ? DarkTheme : LightTheme}>
    <CssBaseline />
    <StyledEngineProvider injectFirst >
      <App isDarkTheme={issDarkTheme} themeChanger={setIsDarkTheme}/>
    </StyledEngineProvider>
  </ThemeProvider>
}

export default ThemeIncluder
