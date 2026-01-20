# Tensor Operations

PyTorch supports a wide variety of tensor operations for mathematical computations.

## Tasks

Implement the following functions in `src/main.py`:

### 1. `add_tensors(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor`
Add two tensors element-wise.

### 2. `multiply_tensors(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor`
Multiply two tensors element-wise.

### 3. `matrix_multiply(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor`
Perform matrix multiplication on two 2D tensors.

### 4. `reshape_tensor(tensor: torch.Tensor, new_shape: tuple) -> torch.Tensor`
Reshape a tensor to a new shape.

### 5. `sum_tensor(tensor: torch.Tensor) -> torch.Tensor`
Return the sum of all elements in the tensor.

## Example

```python
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

print(add_tensors(a, b))  # tensor([5, 7, 9])
print(multiply_tensors(a, b))  # tensor([4, 10, 18])
```
