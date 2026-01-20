# Props

Learn how to pass data to React components using props.

## Background

Props (properties) are how you pass data from a parent component to a child component. They are read-only.

```tsx
interface GreetingProps {
  name: string;
}

function Greeting({ name }: GreetingProps) {
  return <h1>Hello, {name}!</h1>;
}

// Usage: <Greeting name="Alice" />
```

## Tasks

Create a `UserCard` component in `src/UserCard.tsx` that:

1. Accepts props: `name` (string) and `age` (number)
2. Renders the user's name in an `<h2>` element
3. Renders the user's age in a `<p>` element with text "Age: X"
4. Wraps everything in a `<div>` with className="user-card"

## Expected Output

```html
<div class="user-card">
  <h2>Alice</h2>
  <p>Age: 25</p>
</div>
```

## Example Usage

```tsx
<UserCard name="Alice" age={25} />
```
