import { expect, test } from '@playwright/test';

test('chart interval switching supports all Phase 1 intervals', async ({ page }) => {
  await page.goto('/');

  for (const interval of ['1m', '5m', '15m', '1h']) {
    await page.getByRole('button', { name: interval, exact: true }).click();
    await expect(page.getByRole('heading', { name: new RegExp(`BTC-USD / ${interval}`, 'i') })).toBeVisible();
  }
});
