import type { MarketSummary, ProductId } from '../services/contracts';

export interface MarketTileProps {
  summary: MarketSummary;
  active: boolean;
  onSelect: (productId: ProductId) => void;
}

const freshnessLabels = {
  fresh: 'Fresh',
  stale: 'Stale',
  reconnecting: 'Reconnecting',
  offline: 'Offline',
};

export function formatPrice(value: string): string {
  const number = Number(value);
  if (!Number.isFinite(number)) return '$0.00';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: number >= 1000 ? 2 : 4,
  }).format(number);
}

export function formatChange(value: string): string {
  const number = Number(value.replace('%', ''));
  if (!Number.isFinite(number)) return '0.00%';
  const sign = number > 0 ? '+' : '';
  return `${sign}${number.toFixed(2)}%`;
}

export function MarketTile({ summary, active, onSelect }: MarketTileProps) {
  const changeNumber = Number(summary.price_change_24h_percent.replace('%', ''));
  const changeClass = changeNumber < 0 ? 'negative' : 'positive';

  return (
    <button
      type="button"
      className={`market-tile ${active ? 'active' : ''}`}
      aria-pressed={active}
      aria-label={`${summary.product_id} market tile`}
      onClick={() => onSelect(summary.product_id)}
    >
      <span className="tile-row">
        <strong>{summary.product_id}</strong>
        <span className={`freshness ${summary.freshness}`}>{freshnessLabels[summary.freshness]}</span>
      </span>
      <span className="tile-price">{formatPrice(summary.price)}</span>
      <span className={`tile-change ${changeClass}`}>24h {formatChange(summary.price_change_24h_percent)}</span>
      <span className="tile-updated">{new Date(summary.last_update_at).toLocaleTimeString()}</span>
    </button>
  );
}
