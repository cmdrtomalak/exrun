const { test, expect } = require('@playwright/test');

test('Interactive Components - Button Transitions', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test CTA button has transition
  const ctaButton = page.locator('.cta-button');
  await expect(ctaButton).toBeVisible();
  
  // Check transition property
  const transition = await ctaButton.evaluate(el => 
    window.getComputedStyle(el).transition
  );
  expect(transition).toContain('transform');
  expect(transition).toContain('box-shadow');
  
  // Test hover effect
  await ctaButton.hover();
  
  // Check transform is applied on hover
  const transform = await ctaButton.evaluate(el => 
    window.getComputedStyle(el).transform
  );
  expect(transform).not.toBe('none');
  
  // Check box-shadow is applied on hover
  const boxShadow = await ctaButton.evaluate(el => 
    window.getComputedStyle(el).boxShadow
  );
  expect(boxShadow).not.toBe('none');
});

test('Interactive Components - Card Hover Effects', async ({ page }) => {
  await page.goto('./src/index.html');
  
  const card = page.locator('.interactive-card').first();
  await expect(card).toBeVisible();
  
  // Test card has transition
  const cardTransition = await card.evaluate(el => 
    window.getComputedStyle(el).transition
  );
  expect(cardTransition).toContain('transform');
  
  // Test initial overlay is hidden
  const overlay = card.locator('.card-overlay');
  const initialOpacity = await overlay.evaluate(el => 
    window.getComputedStyle(el).opacity
  );
  expect(initialOpacity).toBe('0');
  
  // Test overlay shows on hover
  await card.hover();
  const hoverOpacity = await overlay.evaluate(el => 
    window.getComputedStyle(el).opacity
  );
  expect(hoverOpacity).toBe('1');
  
  // Test card transform on hover
  const cardTransform = await card.evaluate(el => 
    window.getComputedStyle(el).transform
  );
  expect(cardTransform).not.toBe('none');
});

test('Interactive Components - Navigation Link Effects', async ({ page }) => {
  await page.goto('./src/index.html');
  
  const navLink = page.locator('.nav-link').first();
  await expect(navLink).toBeVisible();
  
  // Test link has transition
  const linkTransition = await navLink.evaluate(el => 
    window.getComputedStyle(el).transition
  );
  expect(linkTransition).toContain('color');
  
  // Test initial ::after pseudo-element width
  const afterWidth = await navLink.evaluate(el => {
    const after = window.getComputedStyle(el, '::after');
    return after.width;
  });
  expect(afterWidth).toBe('0px');
  
  // Test ::after width on hover
  await navLink.hover();
  const hoverAfterWidth = await navLink.evaluate(el => {
    const after = window.getComputedStyle(el, '::after');
    return after.width;
  });
  expect(hoverAfterWidth).not.toBe('0px');
});

test('Interactive Components - Animations', async ({ page }) => {
  await page.goto('./src/index.html');
  
  // Test animated content has animation
  const animatedContent = page.locator('.animated-content');
  const contentAnimation = await animatedContent.evaluate(el => 
    window.getComputedStyle(el).animationName
  );
  expect(contentAnimation).not.toBe('none');
  
  // Test loading spinner has animation
  const spinner = page.locator('.loading-spinner');
  const spinnerAnimation = await spinner.evaluate(el => 
    window.getComputedStyle(el).animationName
  );
  expect(spinnerAnimation).not.toBe('none');
  
  // Test animated logo has hover animation
  const logo = page.locator('.animated-logo');
  await logo.hover();
  const logoAnimation = await logo.evaluate(el => 
    window.getComputedStyle(el).animationName
  );
  expect(logoAnimation).not.toBe('none');
});

test('Interactive Components - Form Interactions', async ({ page }) => {
  await page.goto('./src/index.html');
  
  const formInput = page.locator('.form-input').first();
  const formLabel = page.locator('.form-label').first();
  
  await expect(formInput).toBeVisible();
  await expect(formLabel).toBeVisible();
  
  // Test input has transition
  const inputTransition = await formInput.evaluate(el => 
    window.getComputedStyle(el).transition
  );
  expect(inputTransition).toContain('border-color');
  expect(inputTransition).toContain('box-shadow');
  
  // Test initial label position
  const initialLabelTop = await formLabel.evaluate(el => 
    window.getComputedStyle(el).top
  );
  
  // Test label moves when input is focused
  await formInput.focus();
  const focusedLabelTop = await formLabel.evaluate(el => 
    window.getComputedStyle(el).top
  );
  expect(parseFloat(focusedLabelTop)).toBeLessThan(parseFloat(initialLabelTop));
  
  // Test input border changes on focus
  const inputBorderColor = await formInput.evaluate(el => 
    window.getComputedStyle(el).borderColor
  );
  expect(inputBorderColor).not.toBe('rgb(224, 224, 224)'); // Not the default border color
  
  // Test input has box-shadow on focus
  const inputBoxShadow = await formInput.evaluate(el => 
    window.getComputedStyle(el).boxShadow
  );
  expect(inputBoxShadow).not.toBe('none');
});

test('Interactive Components - Form Submission Loading State', async ({ page }) => {
  await page.goto('./src/index.html');
  
  const form = page.locator('.contact-form');
  const submitBtn = page.locator('.submit-btn');
  const btnText = submitBtn.locator('.btn-text');
  const btnLoader = submitBtn.locator('.btn-loader');
  
  // Fill form
  await form.locator('input[type="text"]').fill('Test Name');
  await form.locator('input[type="email"]').fill('test@example.com');
  await form.locator('textarea').fill('Test message');
  
  // Submit form
  await form.locator('button[type="submit"]').click();
  
  // Test loading state
  await expect(submitBtn).toHaveClass(/loading/);
  await expect(btnText).not.toBeVisible();
  await expect(btnLoader).toBeVisible();
  
  // Wait for submission to complete
  await page.waitForTimeout(2500);
  
  // Test success message appears
  const successMessage = form.locator('div').filter({ hasText: 'Message sent successfully!' });
  await expect(successMessage).toBeVisible();
  
  // Test button returns to normal state
  await expect(submitBtn).not.toHaveClass(/loading/);
  await expect(btnText).toBeVisible();
  await expect(btnLoader).not.toBeVisible();
});

test('Interactive Components - Skill Bar Animations', async ({ page }) => {
  await page.goto('./src/index.html');
  
  const skillProgress = page.locator('.skill-progress').first();
  
  // Test initial transform
  const initialTransform = await skillProgress.evaluate(el => 
    window.getComputedStyle(el).transform
  );
  expect(initialTransform).toBe('matrix(0, 0, 0, 0, 0, 0)'); // scaleX(0)
  
  // Scroll skill bars into view
  await skillProgress.scrollIntoViewIfNeeded();
  
  // Wait for animation to trigger
  await page.waitForTimeout(500);
  
  // Test transform after animation (should be scaled based on data-skill)
  const animatedTransform = await skillProgress.evaluate(el => 
    window.getComputedStyle(el).transform
  );
  expect(animatedTransform).not.toBe('matrix(0, 0, 0, 0, 0, 0)');
  
  // Test skill has transition
  const skillTransition = await skillProgress.evaluate(el => 
    window.getComputedStyle(el).transition
  );
  expect(skillTransition).toContain('transform');
});
