import type { ChartInterval } from '../services/contracts';

export interface IntervalOption {
  id: ChartInterval;
  label: string;
  seconds: number;
}

export const intervalOptions: IntervalOption[] = [
  { id: '1m', label: '1m', seconds: 60 },
  { id: '5m', label: '5m', seconds: 300 },
  { id: '15m', label: '15m', seconds: 900 },
  { id: '1h', label: '1h', seconds: 3600 },
];

export function isChartInterval(value: string): value is ChartInterval {
  return intervalOptions.some((interval) => interval.id === value);
}
