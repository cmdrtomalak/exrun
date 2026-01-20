# Interfaces

Learn to define object shapes with interfaces.

## Background

Interfaces define the structure of objects:

```typescript
interface Person {
  name: string;
  age: number;
  email?: string;  // optional
  readonly id: number;  // can't be changed
}

const alice: Person = {
  id: 1,
  name: "Alice",
  age: 25
};
```

## Tasks

### 1. Define a `Product` interface with:
- `id`: number (readonly)
- `name`: string
- `price`: number
- `description`: string (optional)

### 2. `createProduct(id, name, price, description?) -> Product`
Create and return a Product object.

### 3. `formatProduct(product: Product) -> string`
Return "{name} - ${price}" (e.g., "Widget - $9.99")

### 4. `getTotalPrice(products: Product[]) -> number`
Return the sum of all product prices.

### 5. `filterByPrice(products: Product[], maxPrice: number) -> Product[]`
Return products with price <= maxPrice.

## Example

```typescript
const widget = createProduct(1, "Widget", 9.99, "A useful widget");
formatProduct(widget);  // "Widget - $9.99"

const products = [
  createProduct(1, "A", 10),
  createProduct(2, "B", 20),
  createProduct(3, "C", 15)
];
getTotalPrice(products);  // 45
filterByPrice(products, 15);  // products A and C
```
