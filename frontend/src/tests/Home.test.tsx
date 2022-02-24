import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../pages/Home/Home';

test('renders Home page text', () => {
  render(<Home />);
  const linkElement = screen.getByText(/hello/i);
  expect(linkElement).toBeInTheDocument();
});
