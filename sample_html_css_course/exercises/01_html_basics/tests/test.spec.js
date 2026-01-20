const { test, expect } = require('@playwright/test');

test('HTML Basics - Portfolio Page Structure', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test basic HTML structure
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  await expect(page.locator('head meta[charset="UTF-8"]')).toBeVisible();
  
  // Test semantic elements
  await expect(page.locator('header')).toBeVisible();
  await expect(page.locator('nav')).toBeVisible();
  await expect(page.locator('main')).toBeVisible();
  await expect(page.locator('section')).toHaveCount.atLeast(2);
  await expect(page.locator('footer')).toBeVisible();
  
  // Test heading hierarchy
  await expect(page.locator('h1')).toBeVisible();
  await expect(page.locator('h1')).toContainText(/Portfolio|Your Name/i);
  
  // Test navigation
  await expect(page.locator('nav a')).toHaveCount.atLeast(2);
  
  // Test content elements
  await expect(page.locator('main p')).toHaveCount.atLeast(1);
  await expect(page.locator('main ul')).toHaveCount.atLeast(1);
  await expect(page.locator('main a')).toHaveCount.atLeast(1);
  
  // Test footer
  await expect(page.locator('footer')).toContainText(/©|copyright|20/i);
});

test('HTML Accessibility - Semantic Structure', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Check for proper heading hierarchy
  const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
  expect(headings.length).toBeGreaterThan(1);
  
  // First heading should be h1
  const firstHeading = await headings[0].evaluate(el => el.tagName);
  expect(firstHeading).toBe('H1');
  
  // Test that semantic elements are properly nested
  const header = page.locator('header');
  await expect(header).toContainText(/Portfolio|Your Name/i);
  
  const main = page.locator('main');
  await expect(main).toBeVisible();
  
  const footer = page.locator('footer');
  await expect(footer).toBeVisible();
});
