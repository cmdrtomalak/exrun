# State

Learn how to manage component state with the useState hook.

## Background

State allows components to "remember" information and update the UI when that information changes.

```tsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

## Tasks

Create a `Counter` component in `src/Counter.tsx` that:

1. Uses `useState` to track a count (starting at 0)
2. Displays the current count in a `<span>` with className="count"
3. Has an "Increment" button that increases the count by 1
4. Has a "Decrement" button that decreases the count by 1
5. Has a "Reset" button that sets the count back to 0

## Expected Structure

```html
<div class="counter">
  <span class="count">0</span>
  <button>Increment</button>
  <button>Decrement</button>
  <button>Reset</button>
</div>
```

## Example Behavior

1. Initial count: 0
2. Click "Increment" → count: 1
3. Click "Increment" → count: 2
4. Click "Decrement" → count: 1
5. Click "Reset" → count: 0
