import { useEffect, useRef } from 'react';
import {
  CandlestickSeries,
  HistogramSeries,
  type IChartApi,
  type ISeriesApi,
  type MouseEventParams,
  type SeriesType,
  createChart,
} from 'lightweight-charts';
import type { Candle } from '../services/contracts';
import { toCandlestickData, toVolumeData } from './chartData';

export interface LightweightCandlestickChartProps {
  candles: Candle[];
  updateMode?: 'snapshot' | 'update';
  onInspect: (candle: Candle | null) => void;
}

export function LightweightCandlestickChart({ candles, updateMode = 'snapshot', onInspect }: LightweightCandlestickChartProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleSeriesRef = useRef<ISeriesApi<SeriesType> | null>(null);
  const volumeSeriesRef = useRef<ISeriesApi<SeriesType> | null>(null);

  useEffect(() => {
    if (!containerRef.current) return undefined;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { color: '#111820' },
        textColor: '#9fb1c3',
      },
      grid: {
        vertLines: { color: '#202b36' },
        horzLines: { color: '#202b36' },
      },
      rightPriceScale: {
        borderColor: '#334252',
      },
      timeScale: {
        borderColor: '#334252',
        timeVisible: true,
      },
      width: containerRef.current.clientWidth,
      height: 520,
    });
    chartRef.current = chart;

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#58d99a',
      downColor: '#ff7a7a',
      borderVisible: false,
      wickUpColor: '#58d99a',
      wickDownColor: '#ff7a7a',
    });
    const volumeSeries = chart.addSeries(HistogramSeries, {
      priceFormat: { type: 'volume' },
      priceScaleId: '',
    });
    volumeSeries.priceScale().applyOptions({
      scaleMargins: { top: 0.8, bottom: 0 },
    });
    candleSeriesRef.current = candleSeries;
    volumeSeriesRef.current = volumeSeries;

    candleSeries.setData(toCandlestickData(candles));
    volumeSeries.setData(toVolumeData(candles));
    chart.timeScale().fitContent();

    const onCrosshair = (param: MouseEventParams) => {
      if (!param.time) {
        onInspect(null);
        return;
      }
      const inspected = candles.find((candle) => candle.time === Number(param.time));
      onInspect(inspected ?? null);
    };
    chart.subscribeCrosshairMove(onCrosshair);

    const resize = () => {
      if (containerRef.current) {
        chart.applyOptions({ width: containerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', resize);

    return () => {
      window.removeEventListener('resize', resize);
      chart.unsubscribeCrosshairMove(onCrosshair);
      chart.remove();
      chartRef.current = null;
      candleSeriesRef.current = null;
      volumeSeriesRef.current = null;
    };
  }, [onInspect]);

  useEffect(() => {
    if (!candleSeriesRef.current || !volumeSeriesRef.current) return;
    const candleData = toCandlestickData(candles);
    const volumeData = toVolumeData(candles);
    if (updateMode === 'update' && candleData.length > 0 && volumeData.length > 0) {
      candleSeriesRef.current.update(candleData[candleData.length - 1]);
      volumeSeriesRef.current.update(volumeData[volumeData.length - 1]);
      return;
    }
    candleSeriesRef.current.setData(candleData);
    volumeSeriesRef.current.setData(volumeData);
    chartRef.current?.timeScale().fitContent();
  }, [candles, updateMode]);

  return <div className="chart-canvas" data-testid="candlestick-chart" ref={containerRef} />;
}
