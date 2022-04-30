import { createTheme, CssBaseline, ThemeOptions, ThemeProvider } from "@mui/material";
import React, { useState } from "react"
import App from "~/App";

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
  const themeFromStorage = () => {
    return localStorage.getItem("isDarkTheme") == "true"

  }

  const [isDarkTheme, setIsDarkTheme] = useState(themeFromStorage())

  return <ThemeProvider theme={isDarkTheme ? DarkTheme : LightTheme}>
    <CssBaseline />
    <App isDarkTheme={isDarkTheme} themeChanger={setIsDarkTheme}/>
  </ThemeProvider>
}

export default ThemeIncluder
