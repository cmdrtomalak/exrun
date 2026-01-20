"""Training Loop - Implement the functions below."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleNetwork(nn.Module):
    """Pre-implemented network for this exercise."""

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def create_loss_function() -> nn.Module:
    """Return a cross-entropy loss function."""
    # TODO: Return nn.CrossEntropyLoss()
    pass


def create_optimizer(model: nn.Module, learning_rate: float) -> torch.optim.Optimizer:
    """Create and return an SGD optimizer."""
    # TODO: Return torch.optim.SGD(model.parameters(), lr=learning_rate)
    pass


def train_step(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    inputs: torch.Tensor,
    labels: torch.Tensor,
) -> float:
    """Perform a single training step and return the loss value.
    
    Steps:
    1. Zero the gradients
    2. Forward pass
    3. Compute loss
    4. Backward pass
    5. Update weights
    6. Return loss as a Python float
    """
    # TODO: Implement the training step
    pass


def compute_accuracy(
    model: nn.Module,
    inputs: torch.Tensor,
    labels: torch.Tensor,
) -> float:
    """Compute classification accuracy.
    
    Args:
        model: The neural network
        inputs: Input tensor of shape (batch_size, 784)
        labels: Ground truth labels of shape (batch_size,)
        
    Returns:
        Accuracy as a float between 0 and 1
    """
    # TODO: Implement accuracy computation
    # Hint: Use torch.argmax() to get predicted classes
    # Hint: Compare predictions to labels and compute mean
    pass
