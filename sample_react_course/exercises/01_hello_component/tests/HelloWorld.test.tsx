import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { HelloWorld } from '../src/HelloWorld';

describe('HelloWorld', () => {
  it('renders Hello, World! text', () => {
    render(<HelloWorld />);
    expect(screen.getByText('Hello, World!')).toBeInTheDocument();
  });

  it('has the greeting className', () => {
    render(<HelloWorld />);
    const element = screen.getByText('Hello, World!');
    expect(element).toHaveClass('greeting');
  });

  it('renders a div element', () => {
    render(<HelloWorld />);
    const element = screen.getByText('Hello, World!');
    expect(element.tagName).toBe('DIV');
  });
});
