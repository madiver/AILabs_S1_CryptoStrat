import { expect, test } from '@playwright/test';

test('symbol selection updates chart and OHLCV readout is visible', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByTestId('candlestick-chart')).toBeVisible();
  await page.getByRole('button', { name: /ETH-USD/i }).click();

  await expect(page.getByRole('heading', { name: /ETH-USD \/ 1m/i })).toBeVisible();
  await expect(page.getByLabel(/Candle details/i)).toContainText(/O|Move over/i);
  await expect(page.locator('canvas').first()).toBeVisible();
});
