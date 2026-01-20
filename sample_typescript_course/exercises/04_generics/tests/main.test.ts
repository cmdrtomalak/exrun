import { describe, it, expect } from 'vitest';
import { identity, wrapInArray, getProperty, merge, mapArray } from '../src/main';

describe('Generics', () => {
  describe('identity', () => {
    it('returns numbers unchanged', () => {
      expect(identity(42)).toBe(42);
    });

    it('returns strings unchanged', () => {
      expect(identity('hello')).toBe('hello');
    });

    it('returns objects unchanged', () => {
      const obj = { a: 1 };
      expect(identity(obj)).toBe(obj);
    });
  });

  describe('wrapInArray', () => {
    it('wraps a number in array', () => {
      expect(wrapInArray(42)).toEqual([42]);
    });

    it('wraps a string in array', () => {
      expect(wrapInArray('hello')).toEqual(['hello']);
    });

    it('wraps an object in array', () => {
      const obj = { x: 1 };
      expect(wrapInArray(obj)).toEqual([obj]);
    });
  });

  describe('getProperty', () => {
    it('gets a property from an object', () => {
      expect(getProperty({ x: 1, y: 2 }, 'x')).toBe(1);
    });

    it('works with string properties', () => {
      expect(getProperty({ name: 'Alice' }, 'name')).toBe('Alice');
    });
  });

  describe('merge', () => {
    it('merges two objects', () => {
      const result = merge({ a: 1 }, { b: 2 });
      expect(result).toEqual({ a: 1, b: 2 });
    });

    it('second object overwrites first', () => {
      const result = merge({ a: 1 }, { a: 2 });
      expect(result.a).toBe(2);
    });

    it('preserves all properties', () => {
      const result = merge({ x: 1, y: 2 }, { z: 3 });
      expect(result).toEqual({ x: 1, y: 2, z: 3 });
    });
  });

  describe('mapArray', () => {
    it('maps numbers to strings', () => {
      expect(mapArray([1, 2, 3], x => x.toString())).toEqual(['1', '2', '3']);
    });

    it('doubles numbers', () => {
      expect(mapArray([1, 2, 3], x => x * 2)).toEqual([2, 4, 6]);
    });

    it('handles empty arrays', () => {
      expect(mapArray([], x => x)).toEqual([]);
    });

    it('maps objects', () => {
      const users = [{ name: 'Alice' }, { name: 'Bob' }];
      expect(mapArray(users, u => u.name)).toEqual(['Alice', 'Bob']);
    });
  });
});
