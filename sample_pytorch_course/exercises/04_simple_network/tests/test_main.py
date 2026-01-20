"""Tests for Simple Neural Network."""

import torch
import torch.nn as nn
from main import SimpleNetwork


def test_network_is_module():
    model = SimpleNetwork()
    assert isinstance(model, nn.Module)


def test_network_has_correct_layers():
    model = SimpleNetwork()
    assert hasattr(model, "fc1")
    assert hasattr(model, "fc2")
    assert hasattr(model, "fc3")
    assert isinstance(model.fc1, nn.Linear)
    assert isinstance(model.fc2, nn.Linear)
    assert isinstance(model.fc3, nn.Linear)


def test_layer_dimensions():
    model = SimpleNetwork()
    assert model.fc1.in_features == 784
    assert model.fc1.out_features == 128
    assert model.fc2.in_features == 128
    assert model.fc2.out_features == 64
    assert model.fc3.in_features == 64
    assert model.fc3.out_features == 10


def test_forward_pass_shape():
    model = SimpleNetwork()
    x = torch.randn(32, 784)
    output = model(x)
    assert output.shape == (32, 10)


def test_forward_pass_single_sample():
    model = SimpleNetwork()
    x = torch.randn(1, 784)
    output = model(x)
    assert output.shape == (1, 10)


def test_forward_is_differentiable():
    model = SimpleNetwork()
    x = torch.randn(4, 784, requires_grad=True)
    output = model(x)
    loss = output.sum()
    loss.backward()
    assert x.grad is not None
