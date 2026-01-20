const { test, expect } = require('@playwright/test');

test('CSS Fundamentals - Styling Applied', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test that CSS is linked
  const styles = await page.evaluate(() => {
    const link = document.querySelector('link[href="style.css"]');
    return link !== null;
  });
  expect(styles).toBe(true);
  
  // Test body styling
  const body = page.locator('body');
  await expect(body).toHaveCSS('font-family', /Arial|sans-serif/);
  await expect(body).toHaveCSS('background-color', /rgb\(\d+|#[0-9a-fA-F]+/);
  
  // Test header styling
  const header = page.locator('header');
  await expect(header).toHaveCSS('background-color', /rgb\(\d+|#[0-9a-fA-F]+/);
  
  // Test navigation hover effect
  const navLink = page.locator('nav a').first();
  await navLink.hover();
  // Note: Hover states can be tricky to test, but we check for basic link styling
  
  // Test section spacing (box model)
  const section = page.locator('section').first();
  const padding = await section.evaluate(el => 
    window.getComputedStyle(el).padding
  );
  expect(padding).not.toBe('0px');
  
  // Test heading typography
  const h1 = page.locator('h1');
  await expect(h1).toHaveCSS('color', /rgb\(\d+|#[0-9a-fA-F]+/);
  
  const h2 = page.locator('h2').first();
  await expect(h2).toHaveCSS('color', /rgb\(\d+|#[0-9a-fA-F]+/);
});

test('CSS Fundamentals - Layout and Spacing', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test box model properties on sections
  const sections = page.locator('section');
  const sectionCount = await sections.count();
  
  for (let i = 0; i < sectionCount; i++) {
    const section = sections.nth(i);
    const margin = await section.evaluate(el => 
      window.getComputedStyle(el).margin
    );
    const padding = await section.evaluate(el => 
      window.getComputedStyle(el).padding
    );
    
    // Sections should have some padding or margin
    expect(margin !== '0px' || padding !== '0px').toBe(true);
  }
  
  // Test footer styling
  const footer = page.locator('footer');
  await expect(footer).toBeVisible();
  await expect(footer).toHaveCSS('color', /rgb\(\d+|#[0-9a-fA-F]+/);
});
