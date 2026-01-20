import { describe, it, expect } from 'vitest';
import { Product, createProduct, formatProduct, getTotalPrice, filterByPrice } from '../src/main';

describe('Interfaces', () => {
  describe('createProduct', () => {
    it('creates a product with required fields', () => {
      const product = createProduct(1, 'Widget', 9.99);
      expect(product.id).toBe(1);
      expect(product.name).toBe('Widget');
      expect(product.price).toBe(9.99);
    });

    it('creates a product with optional description', () => {
      const product = createProduct(1, 'Widget', 9.99, 'A useful widget');
      expect(product.description).toBe('A useful widget');
    });
  });

  describe('formatProduct', () => {
    it('formats product as name - $price', () => {
      const product = createProduct(1, 'Widget', 9.99);
      expect(formatProduct(product)).toBe('Widget - $9.99');
    });

    it('handles whole number prices', () => {
      const product = createProduct(1, 'Item', 25);
      expect(formatProduct(product)).toBe('Item - $25');
    });
  });

  describe('getTotalPrice', () => {
    it('sums all product prices', () => {
      const products = [
        createProduct(1, 'A', 10),
        createProduct(2, 'B', 20),
        createProduct(3, 'C', 15)
      ];
      expect(getTotalPrice(products)).toBe(45);
    });

    it('returns 0 for empty array', () => {
      expect(getTotalPrice([])).toBe(0);
    });
  });

  describe('filterByPrice', () => {
    it('filters products by max price', () => {
      const products = [
        createProduct(1, 'Cheap', 5),
        createProduct(2, 'Medium', 15),
        createProduct(3, 'Expensive', 50)
      ];
      const filtered = filterByPrice(products, 20);
      expect(filtered).toHaveLength(2);
      expect(filtered.map(p => p.name)).toEqual(['Cheap', 'Medium']);
    });

    it('includes products at exact max price', () => {
      const products = [createProduct(1, 'Exact', 10)];
      expect(filterByPrice(products, 10)).toHaveLength(1);
    });
  });
});
