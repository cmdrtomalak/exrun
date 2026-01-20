# Functions

Learn to write typed functions with optional and default parameters.

## Background

TypeScript functions can have typed parameters and return types:

```typescript
// Regular function
function add(a: number, b: number): number {
  return a + b;
}

// Arrow function
const multiply = (a: number, b: number): number => a * b;

// Optional parameter
function greet(name?: string): string {
  return `Hello, ${name ?? 'stranger'}!`;
}

// Default parameter
function greet(name: string = 'World'): string {
  return `Hello, ${name}!`;
}
```

## Tasks

Implement the following functions in `src/main.ts`:

### 1. `multiply(a: number, b: number) -> number`
Return the product of a and b.

### 2. `greet(name?: string) -> string`
Return "Hello, {name}!" or "Hello, stranger!" if name is not provided.

### 3. `repeat(str: string, times: number = 1) -> string`
Return the string repeated `times` times. Default is 1.

### 4. `createCounter() -> () => number`
Return a function that increments and returns a counter each time it's called.

## Example

```typescript
multiply(3, 4);        // 12
greet("Alice");        // "Hello, Alice!"
greet();               // "Hello, stranger!"
repeat("ha", 3);       // "hahaha"
repeat("hi");          // "hi"

const counter = createCounter();
counter(); // 1
counter(); // 2
```
