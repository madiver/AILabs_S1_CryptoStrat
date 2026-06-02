import { getCandles } from './apiClient';
import type { CandleSnapshot, ChartInterval, ProductId } from './contracts';
import { generateDemoSnapshot } from '../charts/chartData';

export async function loadCandles(symbol: ProductId, interval: ChartInterval): Promise<CandleSnapshot> {
  try {
    return await getCandles(symbol, interval, 100);
  } catch {
    return generateDemoSnapshot(symbol, interval, 120);
  }
}
