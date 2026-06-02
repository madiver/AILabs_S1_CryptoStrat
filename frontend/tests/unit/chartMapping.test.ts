import { describe, expect, it } from 'vitest';
import { formatVolume, generateDemoSnapshot, toCandlestickData, toVolumeData } from '../../src/charts/chartData';

describe('chart data mapping', () => {
  it('maps candles to candlestick and volume series', () => {
    const snapshot = generateDemoSnapshot('BTC-USD', '1m', 100);

    expect(toCandlestickData(snapshot.candles)).toHaveLength(100);
    expect(toVolumeData(snapshot.candles)).toHaveLength(100);
    expect(snapshot.history_status).toBe('complete');
  });

  it('formats unavailable volume safely', () => {
    expect(formatVolume(null)).toBe('Unavailable');
    expect(formatVolume('12.34567')).toBe('12.3457');
  });
});
