import { expect, test } from '@playwright/test';

test('dashboard renders market tiles and no trading controls', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByText(/market-data-only mode/i)).toBeVisible();
  await expect(page.getByRole('button', { name: /BTC-USD/i })).toBeVisible();
  await expect(page.getByRole('button', { name: /ETH-USD/i })).toBeVisible();
  await expect(page.getByRole('button', { name: /SOL-USD/i })).toBeVisible();
  await expect(page.getByText(/24h/i).first()).toBeVisible();

  await expect(page.getByRole('button', { name: /buy/i })).toHaveCount(0);
  await expect(page.getByRole('button', { name: /sell/i })).toHaveCount(0);
  await expect(page.getByRole('button', { name: /submit order/i })).toHaveCount(0);
});
