import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { UserCard } from '../src/UserCard';

describe('UserCard', () => {
  it('renders the name in an h2', () => {
    render(<UserCard name="Alice" age={25} />);
    const heading = screen.getByRole('heading', { level: 2 });
    expect(heading).toHaveTextContent('Alice');
  });

  it('renders the age in a paragraph', () => {
    render(<UserCard name="Bob" age={30} />);
    expect(screen.getByText('Age: 30')).toBeInTheDocument();
  });

  it('has the user-card className', () => {
    const { container } = render(<UserCard name="Charlie" age={20} />);
    expect(container.querySelector('.user-card')).toBeInTheDocument();
  });

  it('renders different props correctly', () => {
    render(<UserCard name="Diana" age={42} />);
    expect(screen.getByText('Diana')).toBeInTheDocument();
    expect(screen.getByText('Age: 42')).toBeInTheDocument();
  });
});
