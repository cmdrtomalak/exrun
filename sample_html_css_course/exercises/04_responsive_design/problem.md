# Responsive Design

Create websites that work beautifully on all devices and screen sizes.

## Background

Responsive design ensures your website looks and functions well on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen orientations

## Tasks

Make your portfolio fully responsive with mobile-first design:

### 1. Viewport Meta Tag
- Add the viewport meta tag for proper mobile rendering
- Set initial-scale=1.0 for consistent scaling

### 2. Mobile-First CSS
- Start with mobile styles as default
- Use min-width media queries for larger screens
- Apply progressive enhancement approach

### 3. Media Query Breakpoints
- Mobile: < 768px (default styles)
- Tablet: 768px - 1024px
- Desktop: > 1024px
- Large desktop: > 1200px

### 4. Responsive Components
- Navigation that adapts to screen size
- Responsive grid layouts
- Flexible typography
- Scalable images and media

### 5. Relative Units
- Use rem/em for typography
- Use percentages for widths
- Use vw/vh for viewport-based sizing

## Example Media Query Structure

```css
/* Mobile-first base styles */
body {
    font-size: 16px; /* Base font size */
    line-height: 1.5;
    padding: 1rem;
}

/* Tablet styles */
@media (min-width: 768px) {
    body {
        font-size: 18px;
        padding: 2rem;
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
    }
}

/* Desktop styles */
@media (min-width: 1024px) {
    body {
        font-size: 20px;
        padding: 3rem;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
}
```

## Viewport Meta Tag

Add this to your HTML `<head>`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
