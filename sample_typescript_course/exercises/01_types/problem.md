# Basic Types

Learn TypeScript's fundamental type annotations.

## Background

TypeScript adds static types to JavaScript. You annotate variables with types using a colon:

```typescript
let name: string = "Alice";
let age: number = 25;
let isActive: boolean = true;
let numbers: number[] = [1, 2, 3];
```

## Tasks

Implement the following functions in `src/main.ts`:

### 1. `formatGreeting(name: string, age: number) -> string`
Return a greeting like "Hello, Alice! You are 25 years old."

### 2. `sumArray(numbers: number[]) -> number`
Return the sum of all numbers in the array.

### 3. `isEven(n: number) -> boolean`
Return true if n is even, false otherwise.

### 4. `getFirstAndLast<T>(arr: T[]) -> [T, T]`
Return a tuple with the first and last elements of the array.

## Example

```typescript
formatGreeting("Bob", 30);  // "Hello, Bob! You are 30 years old."
sumArray([1, 2, 3, 4]);     // 10
isEven(4);                  // true
getFirstAndLast([1, 2, 3]); // [1, 3]
```
