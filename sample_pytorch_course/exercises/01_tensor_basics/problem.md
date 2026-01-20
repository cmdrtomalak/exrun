# Tensor Basics

Tensors are the fundamental data structure in PyTorch. They're similar to NumPy arrays but can run on GPUs.

## Tasks

Implement the following functions in `src/main.py`:

### 1. `create_tensor(data: list) -> torch.Tensor`
Create a tensor from a Python list.

### 2. `create_zeros(shape: tuple) -> torch.Tensor`
Create a tensor filled with zeros of the given shape.

### 3. `create_ones(shape: tuple) -> torch.Tensor`
Create a tensor filled with ones of the given shape.

### 4. `get_shape(tensor: torch.Tensor) -> tuple`
Return the shape of a tensor as a tuple.

## Example

```python
t = create_tensor([1, 2, 3])
print(t)  # tensor([1, 2, 3])

zeros = create_zeros((2, 3))
print(zeros.shape)  # torch.Size([2, 3])
```
