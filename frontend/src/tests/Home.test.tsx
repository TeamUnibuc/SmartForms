import "@testing-library/jest-dom/extend-expect"

import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../pages/Home/Home';

test('renders Home page text', () => {
  // render(<Home />);

  // const rootElement = document.createElement('root')!;
  // const root = createRoot(rootElement);
  // root.render(
  //   <Home />
  // );

  render(<Home />)

  const linkElement = screen.getByText(/Proudly/i);
  expect(linkElement).toBeInTheDocument();
});
