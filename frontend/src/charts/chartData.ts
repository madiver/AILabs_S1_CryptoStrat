import type { CandlestickData, HistogramData, UTCTimestamp } from 'lightweight-charts';
import type { Candle, CandleSnapshot, ChartInterval, ProductId } from '../services/contracts';

const intervalSeconds: Record<ChartInterval, number> = {
  '1m': 60,
  '5m': 300,
  '15m': 900,
  '1h': 3600,
};

const basePrices: Record<ProductId, number> = {
  'BTC-USD': 68450,
  'ETH-USD': 3500,
  'SOL-USD': 150,
};

export function toCandlestickData(candles: Candle[]): CandlestickData[] {
  return candles.map((candle) => ({
    time: candle.time as UTCTimestamp,
    open: Number(candle.open),
    high: Number(candle.high),
    low: Number(candle.low),
    close: Number(candle.close),
  }));
}

export function toVolumeData(candles: Candle[]): HistogramData[] {
  return candles.map((candle) => {
    const open = Number(candle.open);
    const close = Number(candle.close);
    return {
      time: candle.time as UTCTimestamp,
      value: candle.volume === null ? 0 : Number(candle.volume),
      color: close >= open ? 'rgba(88, 217, 154, 0.45)' : 'rgba(255, 122, 122, 0.45)',
    };
  });
}

export function formatVolume(volume: string | null): string {
  if (volume === null) return 'Unavailable';
  const value = Number(volume);
  if (!Number.isFinite(value)) return 'Unavailable';
  return new Intl.NumberFormat('en-US', { maximumFractionDigits: 4 }).format(value);
}

export function generateDemoSnapshot(symbol: ProductId, interval: ChartInterval, count: number): CandleSnapshot {
  const seconds = intervalSeconds[interval];
  const now = Math.floor(Date.now() / 1000);
  const alignedNow = now - (now % seconds);
  const candles: Candle[] = [];
  let lastClose = basePrices[symbol];

  for (let index = count - 1; index >= 0; index -= 1) {
    const time = alignedNow - (index * seconds);
    const drift = Math.sin(index / 8) * (lastClose * 0.0015);
    const open = lastClose;
    const close = open + drift;
    const high = Math.max(open, close) + Math.abs(drift * 0.8);
    const low = Math.min(open, close) - Math.abs(drift * 0.8);
    lastClose = close;
    candles.push({
      product_id: symbol,
      interval,
      time,
      open: open.toFixed(2),
      high: high.toFixed(2),
      low: low.toFixed(2),
      close: close.toFixed(2),
      volume: (10 + Math.abs(drift)).toFixed(4),
      complete: index !== 0,
      source: 'historical',
    });
  }

  return {
    product_id: symbol,
    interval,
    freshness: 'fresh',
    history_status: count >= 100 ? 'complete' : 'partial',
    candles,
  };
}
