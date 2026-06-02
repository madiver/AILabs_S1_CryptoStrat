import { mergeSummaries } from './marketStore';
import type { CandleSnapshot, ConnectionState, DashboardEvent, MarketSummary } from '../services/contracts';

export interface MarketEventState {
  summaries: MarketSummary[];
  snapshot: CandleSnapshot | null;
  connection: ConnectionState;
  chartUpdateMode: 'snapshot' | 'update';
}

export function reduceMarketEvent(state: MarketEventState, event: DashboardEvent): MarketEventState {
  if (event.type === 'market_summary') {
    return {
      ...state,
      summaries: mergeSummaries(state.summaries, [event.payload as MarketSummary]),
    };
  }
  if (event.type === 'candle_snapshot') {
    return {
      ...state,
      snapshot: event.payload as CandleSnapshot,
      chartUpdateMode: 'snapshot',
    };
  }
  if (event.type === 'candle_update' && state.snapshot) {
    const candle = (event.payload as { candle: CandleSnapshot['candles'][number] }).candle;
    const candles = [...state.snapshot.candles];
    const index = candles.findIndex((existing) => existing.time === candle.time);
    if (index >= 0) {
      candles[index] = candle;
    } else {
      candles.push(candle);
    }
    return {
      ...state,
      snapshot: { ...state.snapshot, candles },
      chartUpdateMode: 'update',
    };
  }
  if (event.type === 'connection_state') {
    return { ...state, connection: event.payload as ConnectionState };
  }
  return state;
}
