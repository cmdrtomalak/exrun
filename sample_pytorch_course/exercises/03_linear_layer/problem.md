# Linear Layer

A linear (fully connected) layer is the most fundamental neural network layer.

## Background

A linear layer performs: `y = x @ W.T + b`

Where:
- `x` is the input tensor of shape `(batch_size, in_features)`
- `W` is the weight matrix of shape `(out_features, in_features)`
- `b` is the bias vector of shape `(out_features,)`
- `y` is the output tensor of shape `(batch_size, out_features)`

## Tasks

Implement the following functions in `src/main.py`:

### 1. `create_linear_layer(in_features: int, out_features: int) -> nn.Linear`
Create and return a linear layer with the specified input and output dimensions.

### 2. `get_weight_shape(layer: nn.Linear) -> tuple`
Return the shape of the weight matrix as a tuple.

### 3. `forward_pass(layer: nn.Linear, x: torch.Tensor) -> torch.Tensor`
Run a forward pass through the layer.

### 4. `count_parameters(layer: nn.Linear) -> int`
Count the total number of trainable parameters (weights + biases).

## Example

```python
layer = create_linear_layer(10, 5)
print(get_weight_shape(layer))  # (5, 10)
print(count_parameters(layer))  # 55 (10*5 + 5)
```
