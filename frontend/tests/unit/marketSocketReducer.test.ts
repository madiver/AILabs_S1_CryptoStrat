import { describe, expect, it } from 'vitest';
import { reduceMarketEvent, type MarketEventState } from '../../src/state/marketEvents';
import { demoSummaries } from '../../src/state/marketStore';

const state: MarketEventState = {
  summaries: demoSummaries,
  snapshot: null,
  connection: { status: 'fresh', scope: 'backend' },
  chartUpdateMode: 'snapshot',
};

describe('market event reducer', () => {
  it('applies connection states', () => {
    const next = reduceMarketEvent(state, {
      type: 'connection_state',
      event_id: 'evt',
      occurred_at: new Date().toISOString(),
      payload: { status: 'stale', scope: 'symbol', product_id: 'BTC-USD' },
    });

    expect(next.connection.status).toBe('stale');
  });

  it('applies candle snapshots and updates', () => {
    const snapshotState = reduceMarketEvent(state, {
      type: 'candle_snapshot',
      event_id: 'evt',
      occurred_at: new Date().toISOString(),
      payload: {
        product_id: 'BTC-USD',
        interval: '1m',
        freshness: 'fresh',
        history_status: 'complete',
        candles: [],
      },
    });

    expect(snapshotState.chartUpdateMode).toBe('snapshot');
  });
});
