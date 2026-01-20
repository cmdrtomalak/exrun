# Interactive Components

Add life to your website with CSS animations, transitions, and hover effects.

## Background

Interactive elements make websites more engaging and provide better user feedback through:
- Smooth transitions between states
- Eye-catching animations
- Responsive hover and focus effects
- Loading animations and micro-interactions

## Tasks

Enhance your portfolio with interactive components:

### 1. CSS Transitions
- Add smooth hover transitions to buttons
- Create color transitions for links
- Implement transform transitions (scale, rotate)
- Add opacity transitions for fade effects

### 2. CSS Animations
- Create loading spinners
- Add attention-grabbing animations (pulse, bounce)
- Implement slide-in animations
- Create continuous animation loops

### 3. Hover Effects
- Card lift and shadow effects
- Image zoom and overlay effects
- Button state changes
- Navigation item effects

### 4. Advanced Interactions
- Staggered animations for multiple elements
- Parallax scrolling effects
- Custom cursor interactions
- Loading states and transitions

## Example Animation Syntax

```css
/* Transitions */
.button {
    background-color: #007bff;
    transition: all 0.3s ease;
}

.button:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.card {
    animation: fadeInUp 0.6s ease-out;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

.cta-button {
    animation: pulse 2s infinite;
}
```

## Performance Considerations

- Use `transform` and `opacity` for smooth animations (GPU-accelerated)
- Avoid animating layout properties like `margin`, `padding`
- Use `will-change` sparingly for performance optimization
- Test animations on lower-end devices
