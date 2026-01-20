# CSS Fundamentals

Learn CSS selectors, properties, and styling basics to make your HTML look professional.

## Background

CSS (Cascading Style Sheets) controls the visual presentation of HTML elements. Understanding CSS fundamentals is essential for web development.

## Tasks

Enhance your portfolio page by adding CSS styling in `src/style.css`:

### 1. CSS Selectors
- Use element selectors (h1, p, ul, etc.)
- Create and use class selectors (.class-name)
- Create and use ID selectors (#id-name)
- Use descendant selectors (nav a, section h2)

### 2. Colors and Backgrounds
- Set background colors for the page and sections
- Apply text colors to headings and paragraphs
- Add hover effects to links

### 3. Typography
- Set font families for body text and headings
- Define font sizes for different heading levels
- Set font weights and text alignment

### 4. Box Model Properties
- Add padding to sections and containers
- Set margins for spacing between elements
- Style borders around elements

## Example CSS Structure

```css
/* Global styles */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
    background-color: #f4f4f4;
}

/* Header styling */
header {
    background-color: #333;
    color: white;
    padding: 1rem;
    text-align: center;
}

/* Navigation */
nav a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
}

nav a:hover {
    text-decoration: underline;
}
```

## Link CSS to HTML

Don't forget to link your CSS file in the HTML `<head>`:
```html
<link rel="stylesheet" href="style.css">
```
