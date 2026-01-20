# Layout & Positioning

Master modern CSS layout techniques with Flexbox and Grid.

## Background

Modern CSS provides powerful layout systems:
- **Flexbox**: One-dimensional layouts (rows or columns)
- **Grid**: Two-dimensional layouts (rows and columns)
- **Positioning**: Precise element placement

## Tasks

Create a modern portfolio layout using CSS Grid and Flexbox:

### 1. CSS Grid Layout
- Use Grid for the overall page layout
- Create a responsive grid for project cards
- Define grid areas for header, main, sidebar, footer

### 2. Flexbox Components
- Use Flexbox for navigation bar layout
- Create card layouts with Flexbox
- Align items vertically and horizontally

### 3. Positioning Techniques
- Create a fixed navigation bar
- Position elements relative to their containers
- Add overlay elements or tooltips

### 4. Advanced Layout Features
- Use grid-gap for spacing
- Implement responsive grid layouts
- Create complex layouts with nested grids

## Example Layout Structure

```css
/* Grid Layout */
body {
    display: grid;
    grid-template-areas: 
        "header header"
        "sidebar main"
        "footer footer";
    grid-template-columns: 250px 1fr;
    min-height: 100vh;
}

/* Flexbox Navigation */
nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Card Layout */
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.card {
    display: flex;
    flex-direction: column;
}
```
