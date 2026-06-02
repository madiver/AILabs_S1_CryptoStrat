export type ProductId = 'BTC-USD' | 'ETH-USD' | 'SOL-USD';
export type ChartInterval = '1m' | '5m' | '15m' | '1h';
export type Freshness = 'fresh' | 'stale' | 'reconnecting' | 'offline';
export type HistoryStatus = 'complete' | 'partial' | 'unavailable';
export type CandleSource = 'historical' | 'live' | 'backfill';
export type DashboardEventType =
  | 'market_summary'
  | 'candle_snapshot'
  | 'candle_update'
  | 'connection_state'
  | 'error';

export interface MarketSymbol {
  product_id: ProductId;
  base_currency: string;
  quote_currency: 'USD';
  display_name: string;
  enabled: boolean;
}

export interface MarketSummary {
  product_id: ProductId;
  price: string;
  price_change_24h_percent: string;
  last_update_at: string;
  freshness: Freshness;
}

export interface Candle {
  product_id: ProductId;
  interval: ChartInterval;
  time: number;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string | null;
  complete: boolean;
  source: CandleSource;
}

export interface CandleSnapshot {
  product_id: ProductId;
  interval: ChartInterval;
  freshness: Freshness;
  history_status: HistoryStatus;
  candles: Candle[];
}

export interface ConnectionState {
  status: Freshness;
  scope: 'backend' | 'coinbase' | 'symbol' | 'chart';
  product_id?: ProductId;
  interval?: ChartInterval;
  last_update_at?: string;
  last_heartbeat_at?: string;
  reason?: string;
}

export interface DashboardEvent<TPayload = unknown> {
  type: DashboardEventType;
  event_id: string;
  occurred_at: string;
  payload: TPayload;
}

export interface HealthResponse {
  mode: 'market-data-only';
  backend_status: Freshness;
  trading_enabled: false;
  generated_at?: string;
}
