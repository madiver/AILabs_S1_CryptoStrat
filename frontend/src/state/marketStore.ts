import type { ChartInterval, MarketSummary, ProductId } from '../services/contracts';

export const SUPPORTED_SYMBOLS: ProductId[] = ['BTC-USD', 'ETH-USD', 'SOL-USD'];
export const DEFAULT_SYMBOL: ProductId = 'BTC-USD';
export const DEFAULT_INTERVAL: ChartInterval = '1m';

export const demoSummaries: MarketSummary[] = [
  {
    product_id: 'BTC-USD',
    price: '68450.12',
    price_change_24h_percent: '2.13',
    last_update_at: new Date().toISOString(),
    freshness: 'fresh',
  },
  {
    product_id: 'ETH-USD',
    price: '3500.10',
    price_change_24h_percent: '-1.50',
    last_update_at: new Date().toISOString(),
    freshness: 'fresh',
  },
  {
    product_id: 'SOL-USD',
    price: '150.25',
    price_change_24h_percent: '0.24',
    last_update_at: new Date().toISOString(),
    freshness: 'fresh',
  },
];

export function mergeSummaries(current: MarketSummary[], incoming: MarketSummary[]): MarketSummary[] {
  const bySymbol = new Map(current.map((summary) => [summary.product_id, summary]));
  for (const summary of incoming) {
    bySymbol.set(summary.product_id, summary);
  }
  return SUPPORTED_SYMBOLS.map((symbol) => bySymbol.get(symbol)).filter(Boolean) as MarketSummary[];
}
