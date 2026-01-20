import { describe, it, expect } from 'vitest';
import { formatGreeting, sumArray, isEven, getFirstAndLast } from '../src/main';

describe('Basic Types', () => {
  describe('formatGreeting', () => {
    it('formats a greeting with name and age', () => {
      expect(formatGreeting('Alice', 25)).toBe('Hello, Alice! You are 25 years old.');
    });

    it('works with different values', () => {
      expect(formatGreeting('Bob', 30)).toBe('Hello, Bob! You are 30 years old.');
    });
  });

  describe('sumArray', () => {
    it('sums an array of numbers', () => {
      expect(sumArray([1, 2, 3, 4])).toBe(10);
    });

    it('returns 0 for empty array', () => {
      expect(sumArray([])).toBe(0);
    });

    it('handles negative numbers', () => {
      expect(sumArray([1, -2, 3])).toBe(2);
    });
  });

  describe('isEven', () => {
    it('returns true for even numbers', () => {
      expect(isEven(4)).toBe(true);
      expect(isEven(0)).toBe(true);
    });

    it('returns false for odd numbers', () => {
      expect(isEven(3)).toBe(false);
      expect(isEven(1)).toBe(false);
    });
  });

  describe('getFirstAndLast', () => {
    it('returns first and last elements', () => {
      expect(getFirstAndLast([1, 2, 3])).toEqual([1, 3]);
    });

    it('works with strings', () => {
      expect(getFirstAndLast(['a', 'b', 'c'])).toEqual(['a', 'c']);
    });

    it('handles single element array', () => {
      expect(getFirstAndLast([42])).toEqual([42, 42]);
    });
  });
});
