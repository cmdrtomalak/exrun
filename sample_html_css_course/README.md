# Learn HTML & CSS

A comprehensive, hands-on tutorial for learning modern HTML5 and CSS3 through progressive exercises.

## Overview

This course teaches web development fundamentals through 5 carefully designed exercises that build upon each other:

1. **HTML Basics** - Semantic HTML5 structure and elements
2. **CSS Fundamentals** - Selectors, properties, typography, and the box model
3. **Layout & Positioning** - Flexbox, CSS Grid, and modern positioning
4. **Responsive Design** - Mobile-first design with media queries
5. **Interactive Components** - Animations, transitions, and micro-interactions

## Getting Started

### Prerequisites

- Node.js (for Playwright testing)
- The `exrun` exercise runner

### Setup

```bash
# Navigate to the course directory
cd sample_html_css_course

# Install dependencies (Playwright)
npm install

# Install Playwright browsers
npx playwright install

# Start the tutorial in watch mode
uv run exrun watch
```

### Usage

```bash
# List all exercises
uv run exrun list

# Run current exercise
uv run exrun run

# Run specific exercise
uv run exrun run 01_html_basics

# Check your progress
uv run exrun status

# Reset an exercise
uv run exrun reset 01_html_basics

# Get hints after failed attempts
uv run exrun run --hint
```

## Course Structure

### Exercise 1: HTML Basics
Learn semantic HTML5 structure including:
- HTML5 boilerplate
- Semantic elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- Proper heading hierarchy
- Accessibility best practices

**Outcome:** A well-structured portfolio page with semantic HTML

### Exercise 2: CSS Fundamentals
Master CSS basics:
- Selectors (element, class, ID, descendant)
- Colors and backgrounds
- Typography and fonts
- Box model (margin, padding, border)
- Link styling

**Outcome:** A visually styled portfolio with professional CSS

### Exercise 3: Layout & Positioning
Modern CSS layout techniques:
- CSS Grid for page layouts
- Flexbox for component layouts
- Fixed positioning
- Responsive grid systems

**Outcome:** A modern portfolio with Grid and Flexbox layouts

### Exercise 4: Responsive Design
Mobile-first responsive design:
- Viewport meta tag
- Media queries and breakpoints
- Fluid typography
- Flexible layouts
- Mobile navigation

**Outcome:** A fully responsive portfolio that works on all devices

### Exercise 5: Interactive Components
Add life to your website:
- CSS transitions
- Animations and keyframes
- Hover effects
- Form interactions
- Performance considerations

**Outcome:** An engaging portfolio with smooth animations and interactions

## Learning Approach

### Progressive Learning
Each exercise builds upon previous concepts:
- Start with HTML structure
- Add visual styling
- Implement modern layouts
- Make it responsive
- Add interactivity

### Hands-On Practice
- Real-world projects (portfolio, cards, forms)
- Immediate visual feedback
- Comprehensive test coverage
- Progressive hints system

### Modern Best Practices
- Semantic HTML5
- Mobile-first responsive design
- CSS Grid and Flexbox
- Performance-optimized animations
- Accessibility considerations

## Testing

Each exercise includes comprehensive Playwright tests that verify:
- HTML structure and semantics
- CSS styling and layout
- Responsive behavior
- Interactive functionality
- Accessibility features

Tests run automatically when you save files in watch mode.

## Tips for Success

1. **Read the problem description carefully** - Each exercise has detailed instructions and examples
2. **Use the hints** - After 3 failed attempts, progressive hints are available
3. **Experiment** - Try different approaches and see what works
4. **Test manually** - Open your HTML file in a browser to see visual results
5. **Build incrementally** - Complete one task at a time and test as you go

## Browser Testing

You can test your exercises manually:
1. Open the HTML file in a browser
2. Use browser DevTools to inspect elements
3. Test responsive design with DevTools device emulation
4. Check console for any JavaScript errors

## What You'll Learn

After completing this course, you'll be able to:
- Write semantic, accessible HTML5
- Style websites with modern CSS
- Create responsive layouts with Grid and Flexbox
- Add smooth animations and interactions
- Follow web development best practices
- Build real-world web projects

## Next Steps

After mastering HTML & CSS, consider:
- JavaScript for interactivity
- React or Vue for component-based development
- CSS frameworks like Tailwind CSS
- Backend development with Node.js
- Full-stack web development

## Troubleshooting

### Tests Not Running
- Ensure `npm install` was run successfully
- Install Playwright browsers: `npx playwright install`

### Visual Issues
- Check CSS file is linked in HTML
- Verify file paths are correct
- Use browser DevTools to inspect styles

### Responsive Problems
- Check viewport meta tag is included
- Verify media query syntax
- Test with different viewport sizes

Enjoy learning HTML & CSS! 🚀
