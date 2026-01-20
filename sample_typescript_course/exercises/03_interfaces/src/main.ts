// TODO: Define the Product interface and implement the functions

export interface Product {
  readonly id: number;
  name: string;
  price: number;
  description?: string;
}

export function createProduct(
  id: number,
  name: string,
  price: number,
  description?: string
): Product {
  // TODO: Create and return a Product object
  return {} as Product;
}

export function formatProduct(product: Product): string {
  // TODO: Return "{name} - ${price}"
  return "";
}

export function getTotalPrice(products: Product[]): number {
  // TODO: Return sum of all prices
  return 0;
}

export function filterByPrice(products: Product[], maxPrice: number): Product[] {
  // TODO: Return products with price <= maxPrice
  return [];
}
