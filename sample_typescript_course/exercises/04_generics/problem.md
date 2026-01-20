# Generics

Learn to write reusable, type-safe functions with generics.

## Background

Generics let you write functions that work with any type while preserving type information:

```typescript
// Without generics - loses type info
function identity(value: any): any {
  return value;
}

// With generics - preserves type
function identity<T>(value: T): T {
  return value;
}

const num = identity(42);      // num is number
const str = identity("hello"); // str is string
```

## Tasks

Implement the following generic functions in `src/main.ts`:

### 1. `identity<T>(value: T) -> T`
Return the value unchanged.

### 2. `wrapInArray<T>(value: T) -> T[]`
Return the value wrapped in an array.

### 3. `getProperty<T, K extends keyof T>(obj: T, key: K) -> T[K]`
Return the value of a property from an object.

### 4. `merge<T, U>(obj1: T, obj2: U) -> T & U`
Merge two objects into one.

### 5. `mapArray<T, U>(arr: T[], fn: (item: T) => U) -> U[]`
Apply a function to each element and return new array.

## Example

```typescript
identity(42);           // 42
wrapInArray("hello");   // ["hello"]
getProperty({ x: 1 }, "x");  // 1
merge({ a: 1 }, { b: 2 });   // { a: 1, b: 2 }
mapArray([1, 2, 3], x => x * 2);  // [2, 4, 6]
```
