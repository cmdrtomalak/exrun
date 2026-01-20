import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Counter } from '../src/Counter';

describe('Counter', () => {
  it('renders with initial count of 0', () => {
    render(<Counter />);
    expect(screen.getByText('0')).toBeInTheDocument();
  });

  it('has the count className on the count display', () => {
    render(<Counter />);
    const countElement = screen.getByText('0');
    expect(countElement).toHaveClass('count');
  });

  it('increments the count when Increment is clicked', () => {
    render(<Counter />);
    const incrementBtn = screen.getByText('Increment');
    
    fireEvent.click(incrementBtn);
    expect(screen.getByText('1')).toBeInTheDocument();
    
    fireEvent.click(incrementBtn);
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  it('decrements the count when Decrement is clicked', () => {
    render(<Counter />);
    const incrementBtn = screen.getByText('Increment');
    const decrementBtn = screen.getByText('Decrement');
    
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(decrementBtn);
    
    expect(screen.getByText('1')).toBeInTheDocument();
  });

  it('resets the count when Reset is clicked', () => {
    render(<Counter />);
    const incrementBtn = screen.getByText('Increment');
    const resetBtn = screen.getByText('Reset');
    
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(resetBtn);
    
    expect(screen.getByText('0')).toBeInTheDocument();
  });

  it('has the counter className on the wrapper', () => {
    const { container } = render(<Counter />);
    expect(container.querySelector('.counter')).toBeInTheDocument();
  });
});
