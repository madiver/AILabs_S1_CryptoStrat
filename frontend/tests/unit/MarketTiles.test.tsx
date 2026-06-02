import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { MarketModeBanner } from '../../src/components/MarketModeBanner';
import { MarketTileGrid } from '../../src/components/MarketTileGrid';
import type { MarketSummary, ProductId } from '../../src/services/contracts';

const summaries: MarketSummary[] = [
  {
    product_id: 'BTC-USD',
    price: '68450.12',
    price_change_24h_percent: '2.13',
    last_update_at: '2026-06-02T12:00:00Z',
    freshness: 'fresh',
  },
  {
    product_id: 'ETH-USD',
    price: '3500.10',
    price_change_24h_percent: '-1.50',
    last_update_at: '2026-06-02T12:00:00Z',
    freshness: 'stale',
  },
  {
    product_id: 'SOL-USD',
    price: '150.25',
    price_change_24h_percent: '0.24',
    last_update_at: '2026-06-02T12:00:00Z',
    freshness: 'fresh',
  },
];

describe('MarketTiles', () => {
  it('renders supported market summaries and freshness', () => {
    render(<MarketTileGrid activeSymbol="BTC-USD" summaries={summaries} onSelect={vi.fn()} />);

    expect(screen.getByRole('button', { name: /BTC-USD/i })).toHaveTextContent('$68,450.12');
    expect(screen.getByRole('button', { name: /ETH-USD/i })).toHaveTextContent('Stale');
    expect(screen.getByRole('button', { name: /SOL-USD/i })).toHaveTextContent('24h');
  });

  it('calls onSelect with the selected product', async () => {
    const onSelect = vi.fn<(productId: ProductId) => void>();
    render(<MarketTileGrid activeSymbol="BTC-USD" summaries={summaries} onSelect={onSelect} />);

    screen.getByRole('button', { name: /ETH-USD/i }).click();

    expect(onSelect).toHaveBeenCalledWith('ETH-USD');
  });

  it('renders explicit market data only mode', () => {
    render(<MarketModeBanner />);

    expect(screen.getByText(/market-data-only/i)).toBeInTheDocument();
    expect(screen.getByText(/trading is disabled/i)).toBeInTheDocument();
  });
});
