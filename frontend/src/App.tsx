import { useEffect, useState } from 'react';
import { LightweightCandlestickChart } from './charts/LightweightCandlestickChart';
import { generateDemoSnapshot } from './charts/chartData';
import { CandleReadout } from './components/CandleReadout';
import { ConnectionStatus } from './components/ConnectionStatus';
import { IntervalSelector } from './components/IntervalSelector';
import { MarketModeBanner } from './components/MarketModeBanner';
import { MarketTileGrid } from './components/MarketTileGrid';
import { getMarketSummaries } from './services/apiClient';
import { loadCandles } from './services/candleService';
import { MarketSocket } from './services/marketSocket';
import type { Candle, CandleSnapshot, ConnectionState, MarketSummary, ProductId } from './services/contracts';
import { DEFAULT_INTERVAL, DEFAULT_SYMBOL, demoSummaries, mergeSummaries } from './state/marketStore';

export function App() {
  const [activeSymbol, setActiveSymbol] = useState<ProductId>(DEFAULT_SYMBOL);
  const [activeInterval, setActiveInterval] = useState(DEFAULT_INTERVAL);
  const [summaries, setSummaries] = useState(demoSummaries);
  const [snapshot, setSnapshot] = useState<CandleSnapshot>(() => generateDemoSnapshot(DEFAULT_SYMBOL, DEFAULT_INTERVAL, 120));
  const [inspectedCandle, setInspectedCandle] = useState<Candle | null>(snapshot.candles.at(-1) ?? null);
  const [connection, setConnection] = useState<ConnectionState>({
    status: 'fresh',
    scope: 'backend',
    reason: 'demo data ready',
  });
  const [chartUpdateMode, setChartUpdateMode] = useState<'snapshot' | 'update'>('snapshot');

  useEffect(() => {
    let cancelled = false;

    getMarketSummaries()
      .then((incoming) => {
        if (!cancelled) {
          setSummaries((current) => mergeSummaries(current, incoming));
        }
      })
      .catch(() => {
        if (!cancelled) {
          setSummaries(demoSummaries);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;
    setSnapshot(generateDemoSnapshot(activeSymbol, activeInterval, 120));
    loadCandles(activeSymbol, activeInterval).then((incoming) => {
      if (!cancelled) {
        setSnapshot(incoming);
        setInspectedCandle(incoming.candles.at(-1) ?? null);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [activeSymbol, activeInterval]);

  useEffect(() => {
    const socket = new MarketSocket({
      onEvent: (event) => {
        if (event.type === 'connection_state') {
          setConnection(event.payload as ConnectionState);
        }
        if (event.type === 'market_summary') {
          setSummaries((current) => mergeSummaries(current, [event.payload as MarketSummary]));
        }
        if (event.type === 'candle_snapshot') {
          const incoming = event.payload as CandleSnapshot;
          setSnapshot(incoming);
          setChartUpdateMode('snapshot');
          setInspectedCandle(incoming.candles.at(-1) ?? null);
        }
        if (event.type === 'candle_update') {
          const candle = (event.payload as { candle: Candle }).candle;
          setSnapshot((current) => {
            const candles = [...current.candles];
            const index = candles.findIndex((existing) => existing.time === candle.time);
            if (index >= 0) candles[index] = candle;
            else candles.push(candle);
            const next = { ...current, candles };
            setInspectedCandle(candle);
            return next;
          });
          setChartUpdateMode('update');
        }
      },
      onState: (state) => {
        if (state === 'closed') {
          setConnection({ status: 'offline', scope: 'backend', reason: 'backend market data socket offline' });
        }
      },
    });
    socket.connect(['BTC-USD', 'ETH-USD', 'SOL-USD'], activeSymbol, activeInterval);
    return () => socket.close();
  }, [activeSymbol, activeInterval]);

  return (
    <main className="dashboard-shell">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">AI in the Lab / Phase 1</p>
          <h1>Crypto Market Dashboard</h1>
        </div>
        <div className="status-pill">Trading disabled</div>
      </header>

      <MarketModeBanner />

      <ConnectionStatus connection={connection} />

      <MarketTileGrid summaries={summaries} activeSymbol={activeSymbol} onSelect={setActiveSymbol} />

      <section className="chart-panel" aria-label="Active chart">
        <header className="panel-header">
          <div>
            <p className="eyebrow">Active chart</p>
            <h2>{activeSymbol} / {activeInterval}</h2>
          </div>
          <IntervalSelector activeInterval={activeInterval} onSelect={setActiveInterval} />
          <span className={`freshness ${snapshot.freshness}`}>{snapshot.history_status}</span>
        </header>
        <LightweightCandlestickChart candles={snapshot.candles} updateMode={chartUpdateMode} onInspect={setInspectedCandle} />
        <CandleReadout candle={inspectedCandle} />
      </section>
    </main>
  );
}
