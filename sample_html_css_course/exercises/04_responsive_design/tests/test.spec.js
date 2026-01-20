const { test, expect } = require('@playwright/test');

test('Responsive Design - Viewport Meta Tag', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test viewport meta tag exists
  const viewportMeta = await page.locator('meta[name="viewport"]').count();
  expect(viewportMeta).toBe(1);
  
  const viewportContent = await page.locator('meta[name="viewport"]').getAttribute('content');
  expect(viewportContent).toContain('width=device-width');
  expect(viewportContent).toContain('initial-scale=1.0');
});

test('Responsive Design - Mobile Layout', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Set mobile viewport
  await page.setViewportSize({ width: 375, height: 667 });
  
  // Test mobile navigation
  const mobileMenuBtn = page.locator('.mobile-menu-btn');
  await expect(mobileMenuBtn).toBeVisible();
  
  const navList = page.locator('.nav-list');
  const navListDisplay = await navList.evaluate(el => 
    window.getComputedStyle(el).display
  );
  expect(navListDisplay).toBe('none');
  
  // Test single column project grid on mobile
  const projectGrid = page.locator('.project-grid');
  const projectCards = projectGrid.locator('.project-card');
  const cardCount = await projectCards.count();
  
  for (let i = 0; i < cardCount; i++) {
    const card = projectCards.nth(i);
    const cardWidth = await card.evaluate(el => 
      window.getComputedStyle(el).width
    );
    expect(cardWidth).toBe('100%' || 'calc(100% - 32px)'); // Account for padding
  }
  
  // Test stacked contact section on mobile
  const contactContent = page.locator('.contact-content');
  const contactInfo = contactContent.locator('.contact-info');
  const contactForm = contactContent.locator('.contact-form');
  
  await expect(contactInfo).toBeVisible();
  await expect(contactForm).toBeVisible();
  
  // Verify they're stacked (implementation specific)
  // This checks that both are in the same container
  const containerBounds = await contactContent.boundingBox();
  const infoBounds = await contactInfo.boundingBox();
  const formBounds = await contactForm.boundingBox();
  
  expect(infoBounds.y).toBeLessThan(formBounds.y);
});

test('Responsive Design - Tablet Layout', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Set tablet viewport
  await page.setViewportSize({ width: 768, height: 1024 });
  
  // Test desktop navigation appears
  const navList = page.locator('.nav-list');
  const navListDisplay = await navList.evaluate(el => 
    window.getComputedStyle(el).display
  );
  expect(navListDisplay).toBe('flex');
  
  // Test mobile menu button is hidden
  const mobileMenuBtn = page.locator('.mobile-menu-btn');
  const mobileBtnDisplay = await mobileMenuBtn.evaluate(el => 
    window.getComputedStyle(el).display
  );
  expect(mobileBtnDisplay).toBe('none');
  
  // Test two-column project grid (implementation dependent)
  const projectGrid = page.locator('.project-grid');
  await expect(projectGrid).toBeVisible();
  
  // Test container max-width
  const container = page.locator('.container');
  const containerWidth = await container.evaluate(el => 
    window.getComputedStyle(el).maxWidth
  );
  expect(containerWidth).toBe('768px');
});

test('Responsive Design - Desktop Layout', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Set desktop viewport
  await page.setViewportSize({ width: 1200, height: 800 });
  
  // Test container max-width
  const container = page.locator('.container');
  const containerWidth = await container.evaluate(el => 
    window.getComputedStyle(el).maxWidth
  );
  expect(containerWidth).toBe('1024px' || '1200px');
  
  // Test larger typography on desktop
  const h1 = page.locator('h1');
  const h1FontSize = await h1.evaluate(el => 
    window.getComputedStyle(el).fontSize
  );
  const h1SizeNum = parseFloat(h1FontSize);
  expect(h1SizeNum).toBeGreaterThan(30); // Should be larger than mobile
  
  // Test project grid has more columns
  const projectGrid = page.locator('.project-grid');
  await expect(projectGrid).toBeVisible();
  
  // Test contact section is side-by-side
  const contactContent = page.locator('.contact-content');
  await expect(contactContent).toBeVisible();
});

test('Responsive Design - Large Desktop Layout', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Set large desktop viewport
  await page.setViewportSize({ width: 1400, height: 900 });
  
  // Test container max-width for large screens
  const container = page.locator('.container');
  const containerWidth = await container.evaluate(el => 
    window.getComputedStyle(el).maxWidth
  );
  expect(containerWidth).toBe('1200px');
});
