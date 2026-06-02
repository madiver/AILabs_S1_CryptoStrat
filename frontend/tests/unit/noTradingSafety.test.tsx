import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { App } from '../../src/App';

describe('market-data-only safety', () => {
  it('renders disabled trading mode without trading actions', () => {
    render(<App />);

    expect(screen.getByText(/market-data-only mode/i)).toBeInTheDocument();
    expect(screen.getByText(/trading is disabled/i)).toBeInTheDocument();

    for (const label of [/buy/i, /sell/i, /submit order/i, /paper trade/i, /live trade/i]) {
      expect(screen.queryByRole('button', { name: label })).not.toBeInTheDocument();
    }
  });
});
