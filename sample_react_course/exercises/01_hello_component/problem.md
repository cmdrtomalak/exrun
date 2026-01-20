# Hello Component

Create your first React component!

## Background

React components are functions that return JSX (JavaScript XML). JSX looks like HTML but is actually JavaScript.

```tsx
function MyComponent() {
  return <div>Hello!</div>;
}
```

## Tasks

Create a component called `HelloWorld` in `src/HelloWorld.tsx` that:

1. Returns a `<div>` element
2. The div should contain the text "Hello, World!"
3. The div should have a className of "greeting"

## Expected Output

```html
<div class="greeting">Hello, World!</div>
```

## Example Usage

```tsx
import { HelloWorld } from './HelloWorld';

function App() {
  return <HelloWorld />;
}
```
