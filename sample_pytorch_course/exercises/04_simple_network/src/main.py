"""Simple Neural Network - Implement the class below."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleNetwork(nn.Module):
    """A simple 3-layer neural network for MNIST classification."""

    def __init__(self):
        super().__init__()
        # TODO: Define three linear layers:
        # self.fc1: 784 -> 128
        # self.fc2: 128 -> 64
        # self.fc3: 64 -> 10
        pass

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network.
        
        Args:
            x: Input tensor of shape (batch_size, 784)
            
        Returns:
            Output tensor of shape (batch_size, 10)
        """
        # TODO: Implement the forward pass
        # Apply ReLU after fc1 and fc2, but not after fc3
        # Hint: Use F.relu() or torch.relu()
        pass
