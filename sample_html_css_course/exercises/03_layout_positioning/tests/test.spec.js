const { test, expect } = require('@playwright/test');

test('Layout & Positioning - CSS Grid Implementation', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test body has grid layout
  const body = page.locator('body');
  const bodyDisplay = await body.evaluate(el => 
    window.getComputedStyle(el).display
  );
  expect(bodyDisplay).toBe('grid');
  
  // Test main grid structure
  const mainGrid = page.locator('.main-grid');
  await expect(mainGrid).toBeVisible();
  
  const mainGridDisplay = await mainGrid.evaluate(el => 
    window.getComputedStyle(el).display
  );
  expect(mainGridDisplay).toBe('grid');
  
  // Test project grid
  const projectGrid = page.locator('.project-grid');
  await expect(projectGrid).toBeVisible();
  
  const projectGridDisplay = await projectGrid.evaluate(el => 
    window.getComputedStyle(el).display
  );
  expect(projectGridDisplay).toBe('grid');
});

test('Layout & Positioning - Flexbox Components', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test navigation uses flexbox
  const navbar = page.locator('.navbar');
  const navbarDisplay = await navbar.evaluate(el => 
    window.getComputedStyle(el).display
  );
  expect(navbarDisplay).toBe('flex');
  
  // Test project cards use flexbox
  const projectCards = page.locator('.project-card');
  const cardCount = await projectCards.count();
  
  for (let i = 0; i < cardCount; i++) {
    const card = projectCards.nth(i);
    const cardDisplay = await card.evaluate(el => 
      window.getComputedStyle(el).display
    );
    expect(cardDisplay).toBe('flex');
  }
  
  // Test tech stack uses flexbox
  const techStacks = page.locator('.tech-stack');
  const stackCount = await techStacks.count();
  
  for (let i = 0; i < stackCount; i++) {
    const stack = techStacks.nth(i);
    const stackDisplay = await stack.evaluate(el => 
      window.getComputedStyle(el).display
    );
    expect(stackDisplay).toBe('flex');
  }
});

test('Layout & Positioning - Fixed Navigation', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test navbar is fixed
  const navbar = page.locator('.navbar');
  await expect(navbar).toHaveCSS('position', 'fixed');
  await expect(navbar).toHaveCSS('top', '0px');
  await expect(navbar).toHaveCSS('width', '100%');
  
  // Test navbar is always visible on scroll
  await page.evaluate(() => window.scrollTo(0, 1000));
  await expect(navbar).toBeVisible();
});

test('Layout & Positioning - Responsive Layout', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test desktop layout
  const sidebar = page.locator('.sidebar');
  await expect(sidebar).toBeVisible();
  
  // Test mobile layout
  await page.setViewportSize({ width: 768, height: 1024 });
  
  // Check if layout adapts (implementation dependent)
  // This test assumes responsive styles are applied
  const mainGrid = page.locator('.main-grid');
  await expect(mainGrid).toBeVisible();
});
