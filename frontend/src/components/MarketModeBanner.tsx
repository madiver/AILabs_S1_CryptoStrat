export function MarketModeBanner() {
  return (
    <section className="mode-banner" aria-label="Market data only mode">
      <div>
        <strong>Market-data-only mode</strong>
        <span>No authentication, no account access, and no trading execution.</span>
      </div>
      <p>Trading is disabled. No orders, balances, positions, paper trading, or live trading controls are available.</p>
    </section>
  );
}
