import { expect, test } from '@playwright/test';

test('dashboard remains operable on a narrow viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto('/');

  await expect(page.getByText(/market-data-only mode/i)).toBeVisible();
  await expect(page.getByRole('button', { name: /BTC-USD/i })).toBeVisible();
  await expect(page.getByTestId('candlestick-chart')).toBeVisible();

  const hasHorizontalOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(hasHorizontalOverflow).toBe(false);
});
