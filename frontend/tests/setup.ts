import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

vi.mock('lightweight-charts', async () => {
  const series = {
    setData: vi.fn(),
    update: vi.fn(),
    priceScale: () => ({ applyOptions: vi.fn() }),
  };
  return {
    CandlestickSeries: 'CandlestickSeries',
    HistogramSeries: 'HistogramSeries',
    createChart: vi.fn(() => ({
      addSeries: vi.fn(() => series),
      timeScale: () => ({ fitContent: vi.fn() }),
      subscribeCrosshairMove: vi.fn(),
      unsubscribeCrosshairMove: vi.fn(),
      applyOptions: vi.fn(),
      remove: vi.fn(),
    })),
  };
});
