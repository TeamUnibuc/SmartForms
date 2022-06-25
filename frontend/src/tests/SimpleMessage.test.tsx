import React from 'react';
import { render, screen } from '@testing-library/react';
// import Home from '../pages/Home/Home';
import SimpleMessage from '../components/SimpleMessage';

test('renders Home page text', () => {
  render(<SimpleMessage color='info' msg='Hello world'/>);
  const linkElement = screen.getByText(/Hello/i);
  expect(linkElement).toBeInTheDocument();
});
