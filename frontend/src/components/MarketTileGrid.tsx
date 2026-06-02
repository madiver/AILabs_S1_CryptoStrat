import type { MarketSummary, ProductId } from '../services/contracts';
import { MarketTile } from './MarketTile';

export interface MarketTileGridProps {
  summaries: MarketSummary[];
  activeSymbol: ProductId;
  onSelect: (productId: ProductId) => void;
}

export function MarketTileGrid({ summaries, activeSymbol, onSelect }: MarketTileGridProps) {
  return (
    <section className="tile-grid" aria-label="Market tiles">
      {summaries.map((summary) => (
        <MarketTile
          key={summary.product_id}
          summary={summary}
          active={summary.product_id === activeSymbol}
          onSelect={onSelect}
        />
      ))}
    </section>
  );
}
