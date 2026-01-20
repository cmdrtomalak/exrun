# Simple Neural Network

Build a multi-layer perceptron (MLP) for classifying MNIST digits.

## Background

Neural networks in PyTorch are built by subclassing `nn.Module`. You define:
1. Layers in `__init__`
2. Forward pass logic in `forward`

## Tasks

Create a class `SimpleNetwork` in `src/main.py` that:

### Architecture
- Input: 784 features (28x28 flattened MNIST image)
- Hidden layer 1: 128 neurons with ReLU activation
- Hidden layer 2: 64 neurons with ReLU activation  
- Output: 10 neurons (one per digit class)

### Required structure:
```python
class SimpleNetwork(nn.Module):
    def __init__(self):
        # Define: self.fc1, self.fc2, self.fc3
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pass through layers with ReLU activations
        # (no activation on the output layer)
```

## Example

```python
model = SimpleNetwork()
x = torch.randn(32, 784)  # batch of 32 images
output = model(x)
print(output.shape)  # torch.Size([32, 10])
```
