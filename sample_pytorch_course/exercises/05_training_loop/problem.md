# Training Loop

Learn to train a neural network with the standard PyTorch training loop.

## Background

Training in PyTorch follows this pattern:
1. Forward pass: `outputs = model(inputs)`
2. Compute loss: `loss = criterion(outputs, labels)`
3. Zero gradients: `optimizer.zero_grad()`
4. Backward pass: `loss.backward()`
5. Update weights: `optimizer.step()`

## Tasks

Implement the following functions in `src/main.py`:

### 1. `create_loss_function() -> nn.Module`
Return a cross-entropy loss function for classification.

### 2. `create_optimizer(model: nn.Module, learning_rate: float) -> torch.optim.Optimizer`
Create and return an SGD optimizer for the model's parameters.

### 3. `train_step(model, optimizer, criterion, inputs, labels) -> float`
Perform a single training step and return the loss value.

### 4. `compute_accuracy(model, inputs, labels) -> float`
Compute classification accuracy (between 0 and 1).

## Example

```python
model = SimpleNetwork()
criterion = create_loss_function()
optimizer = create_optimizer(model, lr=0.01)

inputs = torch.randn(32, 784)
labels = torch.randint(0, 10, (32,))

loss = train_step(model, optimizer, criterion, inputs, labels)
accuracy = compute_accuracy(model, inputs, labels)
```
