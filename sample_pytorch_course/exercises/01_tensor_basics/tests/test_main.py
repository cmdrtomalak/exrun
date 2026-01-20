"""Tests for Tensor Basics."""

import torch
from main import create_tensor, create_zeros, create_ones, get_shape


def test_create_tensor_from_list():
    t = create_tensor([1, 2, 3])
    assert isinstance(t, torch.Tensor)
    assert t.tolist() == [1, 2, 3]


def test_create_tensor_2d():
    t = create_tensor([[1, 2], [3, 4]])
    assert t.shape == (2, 2)
    assert t.tolist() == [[1, 2], [3, 4]]


def test_create_zeros():
    z = create_zeros((3, 4))
    assert z.shape == (3, 4)
    assert torch.all(z == 0)


def test_create_ones():
    o = create_ones((2, 2))
    assert o.shape == (2, 2)
    assert torch.all(o == 1)


def test_get_shape():
    t = torch.randn(3, 4, 5)
    assert get_shape(t) == (3, 4, 5)
