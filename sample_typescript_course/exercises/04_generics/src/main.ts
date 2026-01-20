// TODO: Implement generic functions

export function identity<T>(value: T): T {
  // TODO: Return the value unchanged
  return undefined as T;
}

export function wrapInArray<T>(value: T): T[] {
  // TODO: Return [value]
  return [];
}

export function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  // TODO: Return obj[key]
  return undefined as T[K];
}

export function merge<T, U>(obj1: T, obj2: U): T & U {
  // TODO: Return merged object { ...obj1, ...obj2 }
  return {} as T & U;
}

export function mapArray<T, U>(arr: T[], fn: (item: T) => U): U[] {
  // TODO: Return arr.map(fn)
  return [];
}
