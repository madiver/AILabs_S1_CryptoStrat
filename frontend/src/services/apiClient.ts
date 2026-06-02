import type { CandleSnapshot, ChartInterval, HealthResponse, MarketSummary, MarketSymbol, ProductId } from './contracts';

export const API_BASE = '';

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function getHealth(): Promise<HealthResponse> {
  return getJson<HealthResponse>('/api/health');
}

export async function getSymbols(): Promise<MarketSymbol[]> {
  const body = await getJson<{ symbols: MarketSymbol[] }>('/api/symbols');
  return body.symbols;
}

export async function getMarketSummaries(): Promise<MarketSummary[]> {
  const body = await getJson<{ summaries: MarketSummary[] }>('/api/markets/summary');
  return body.summaries;
}

export async function getCandles(
  symbol: ProductId,
  interval: ChartInterval,
  limit = 100,
): Promise<CandleSnapshot> {
  const params = new URLSearchParams({ symbol, interval, limit: String(limit) });
  return getJson<CandleSnapshot>(`/api/candles?${params.toString()}`);
}
