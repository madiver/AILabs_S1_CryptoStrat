import type { Candle } from '../services/contracts';
import { formatVolume } from '../charts/chartData';
import { formatPrice } from './MarketTile';

export interface CandleReadoutProps {
  candle: Candle | null;
}

export function CandleReadout({ candle }: CandleReadoutProps) {
  if (!candle) {
    return (
      <section className="candle-readout" aria-label="Candle details">
        <span>Move over the chart to inspect OHLCV</span>
      </section>
    );
  }

  return (
    <section className="candle-readout" aria-label="Candle details">
      <span>{new Date(candle.time * 1000).toLocaleString()}</span>
      <span>O {formatPrice(candle.open)}</span>
      <span>H {formatPrice(candle.high)}</span>
      <span>L {formatPrice(candle.low)}</span>
      <span>C {formatPrice(candle.close)}</span>
      <span>V {formatVolume(candle.volume)}</span>
    </section>
  );
}
