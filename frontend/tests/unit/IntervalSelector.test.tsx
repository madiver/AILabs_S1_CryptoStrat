import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { IntervalSelector } from '../../src/components/IntervalSelector';
import { isChartInterval } from '../../src/state/intervals';

describe('IntervalSelector', () => {
  it('renders supported intervals and updates selection', () => {
    const onSelect = vi.fn();

    render(<IntervalSelector activeInterval="1m" onSelect={onSelect} />);
    screen.getByRole('button', { name: '5m' }).click();

    expect(screen.getByRole('button', { name: '1m' })).toHaveAttribute('aria-pressed', 'true');
    expect(onSelect).toHaveBeenCalledWith('5m');
  });

  it('rejects unsupported interval strings', () => {
    expect(isChartInterval('1m')).toBe(true);
    expect(isChartInterval('2m')).toBe(false);
  });
});
