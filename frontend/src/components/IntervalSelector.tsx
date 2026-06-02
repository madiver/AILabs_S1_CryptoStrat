import type { ChartInterval } from '../services/contracts';
import { intervalOptions } from '../state/intervals';

export interface IntervalSelectorProps {
  activeInterval: ChartInterval;
  onSelect: (interval: ChartInterval) => void;
}

export function IntervalSelector({ activeInterval, onSelect }: IntervalSelectorProps) {
  return (
    <div className="interval-selector" role="group" aria-label="Chart interval">
      {intervalOptions.map((interval) => (
        <button
          key={interval.id}
          type="button"
          className={interval.id === activeInterval ? 'active' : ''}
          aria-pressed={interval.id === activeInterval}
          onClick={() => onSelect(interval.id)}
        >
          {interval.label}
        </button>
      ))}
    </div>
  );
}
