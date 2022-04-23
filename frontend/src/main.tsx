import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import App from './App'

// ReactDOM.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
//   document.getElementById('root')
// )


// index.js
import { ThemeProvider } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";
import ThemeIncluder from './components/ThemeIncluder';

const rootElement = document.getElementById("root");
ReactDOM.render(
  <ThemeIncluder />,

  rootElement
);
