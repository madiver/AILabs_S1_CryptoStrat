import { expect, test } from '@playwright/test';

test('connection state and stale-data language are visible', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByLabel(/Connection status/i)).toBeVisible();
  await expect(page.getByText(/Healthy|Stale|Reconnecting|Offline/i).first()).toBeVisible();
  await expect(page.getByText(/Trading disabled/i)).toBeVisible();
});
