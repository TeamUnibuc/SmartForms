import './index.css'

// ReactDOM.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
//   document.getElementById('root')
// )


// index.js
import ThemeIncluder from './components/General/ThemeIncluder';

import { createRoot } from 'react-dom/client';
const rootElement = document.getElementById('root')!;
const root = createRoot(rootElement);
root.render(
  <ThemeIncluder />
);
