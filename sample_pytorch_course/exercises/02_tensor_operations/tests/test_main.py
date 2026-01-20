"""Tests for Tensor Operations."""

import torch
from main import add_tensors, multiply_tensors, matrix_multiply, reshape_tensor, sum_tensor


def test_add_tensors():
    a = torch.tensor([1, 2, 3])
    b = torch.tensor([4, 5, 6])
    result = add_tensors(a, b)
    assert result.tolist() == [5, 7, 9]


def test_multiply_tensors():
    a = torch.tensor([1, 2, 3])
    b = torch.tensor([4, 5, 6])
    result = multiply_tensors(a, b)
    assert result.tolist() == [4, 10, 18]


def test_matrix_multiply():
    a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float)
    b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float)
    result = matrix_multiply(a, b)
    expected = torch.tensor([[19, 22], [43, 50]], dtype=torch.float)
    assert torch.allclose(result, expected)


def test_reshape_tensor():
    t = torch.arange(12)
    result = reshape_tensor(t, (3, 4))
    assert result.shape == (3, 4)
    assert result[0].tolist() == [0, 1, 2, 3]


def test_sum_tensor():
    t = torch.tensor([1, 2, 3, 4])
    result = sum_tensor(t)
    assert result.item() == 10
