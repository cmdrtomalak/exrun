"""Linear Layer - Implement the functions below."""

import torch
import torch.nn as nn


def create_linear_layer(in_features: int, out_features: int) -> nn.Linear:
    """Create and return a linear layer."""
    # TODO: Return nn.Linear(in_features, out_features)
    pass


def get_weight_shape(layer: nn.Linear) -> tuple:
    """Return the shape of the weight matrix as a tuple."""
    # TODO: Access layer.weight.shape and convert to tuple
    pass


def forward_pass(layer: nn.Linear, x: torch.Tensor) -> torch.Tensor:
    """Run a forward pass through the layer."""
    # TODO: Call the layer with input x: layer(x)
    pass


def count_parameters(layer: nn.Linear) -> int:
    """Count the total number of trainable parameters."""
    # TODO: Sum the number of elements in weight and bias
    # Hint: Use .numel() to get number of elements in a tensor
    pass
