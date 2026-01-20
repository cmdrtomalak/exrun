"""Tests for Linear Layer."""

import torch
import torch.nn as nn
from main import create_linear_layer, get_weight_shape, forward_pass, count_parameters


def test_create_linear_layer():
    layer = create_linear_layer(10, 5)
    assert isinstance(layer, nn.Linear)
    assert layer.in_features == 10
    assert layer.out_features == 5


def test_get_weight_shape():
    layer = nn.Linear(10, 5)
    shape = get_weight_shape(layer)
    assert shape == (5, 10)


def test_forward_pass():
    layer = nn.Linear(10, 5)
    x = torch.randn(32, 10)
    output = forward_pass(layer, x)
    assert output.shape == (32, 5)


def test_forward_pass_single_sample():
    layer = nn.Linear(4, 2)
    x = torch.randn(1, 4)
    output = forward_pass(layer, x)
    assert output.shape == (1, 2)


def test_count_parameters():
    layer = nn.Linear(10, 5)
    params = count_parameters(layer)
    assert params == 55


def test_count_parameters_larger():
    layer = nn.Linear(100, 50)
    params = count_parameters(layer)
    assert params == 5050
