import { describe, it, expect } from 'vitest';
import { multiply, greet, repeat, createCounter } from '../src/main';

describe('Functions', () => {
  describe('multiply', () => {
    it('multiplies two numbers', () => {
      expect(multiply(3, 4)).toBe(12);
    });

    it('handles zero', () => {
      expect(multiply(5, 0)).toBe(0);
    });

    it('handles negative numbers', () => {
      expect(multiply(-2, 3)).toBe(-6);
    });
  });

  describe('greet', () => {
    it('greets with a name', () => {
      expect(greet('Alice')).toBe('Hello, Alice!');
    });

    it('greets stranger when no name provided', () => {
      expect(greet()).toBe('Hello, stranger!');
    });

    it('greets stranger for undefined', () => {
      expect(greet(undefined)).toBe('Hello, stranger!');
    });
  });

  describe('repeat', () => {
    it('repeats string specified times', () => {
      expect(repeat('ha', 3)).toBe('hahaha');
    });

    it('defaults to 1 repetition', () => {
      expect(repeat('hi')).toBe('hi');
    });

    it('handles 0 repetitions', () => {
      expect(repeat('test', 0)).toBe('');
    });
  });

  describe('createCounter', () => {
    it('creates an independent counter', () => {
      const counter = createCounter();
      expect(counter()).toBe(1);
      expect(counter()).toBe(2);
      expect(counter()).toBe(3);
    });

    it('creates multiple independent counters', () => {
      const counter1 = createCounter();
      const counter2 = createCounter();
      
      expect(counter1()).toBe(1);
      expect(counter1()).toBe(2);
      expect(counter2()).toBe(1);
      expect(counter1()).toBe(3);
    });
  });
});
