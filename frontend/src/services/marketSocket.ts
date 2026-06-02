import type { ChartInterval, DashboardEvent, ProductId } from './contracts';

export interface MarketSocketOptions {
  onEvent: (event: DashboardEvent) => void;
  onState?: (state: 'connecting' | 'open' | 'closed') => void;
}

export class MarketSocket {
  private ws: WebSocket | null = null;

  constructor(private readonly options: MarketSocketOptions) {}

  connect(symbols: ProductId[], activeSymbol: ProductId, activeInterval: ChartInterval): void {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    this.options.onState?.('connecting');
    this.ws = new WebSocket(`${protocol}://${window.location.host}/ws/market-data`);
    this.ws.addEventListener('open', () => {
      this.options.onState?.('open');
      this.send({
        type: 'subscribe',
        symbols,
        active_symbol: activeSymbol,
        active_interval: activeInterval,
      });
    });
    this.ws.addEventListener('message', (message) => {
      try {
        this.options.onEvent(JSON.parse(message.data as string) as DashboardEvent);
      } catch {
        // Ignore malformed events so a single bad frame does not break the dashboard.
      }
    });
    this.ws.addEventListener('close', () => this.options.onState?.('closed'));
  }

  setActiveChart(symbol: ProductId, interval: ChartInterval): void {
    this.send({ type: 'set_active_chart', symbol, interval });
  }

  close(): void {
    this.ws?.close();
    this.ws = null;
  }

  private send(payload: unknown): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(payload));
    }
  }
}
