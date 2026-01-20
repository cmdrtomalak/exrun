"""Tests for Training Loop."""

import torch
import torch.nn as nn
from main import (
    SimpleNetwork,
    create_loss_function,
    create_optimizer,
    train_step,
    compute_accuracy,
)


def test_create_loss_function():
    criterion = create_loss_function()
    assert isinstance(criterion, nn.CrossEntropyLoss)


def test_create_optimizer():
    model = SimpleNetwork()
    optimizer = create_optimizer(model, learning_rate=0.01)
    assert isinstance(optimizer, torch.optim.SGD)
    assert optimizer.defaults["lr"] == 0.01


def test_train_step_returns_loss():
    model = SimpleNetwork()
    criterion = create_loss_function()
    optimizer = create_optimizer(model, learning_rate=0.01)

    inputs = torch.randn(16, 784)
    labels = torch.randint(0, 10, (16,))

    loss = train_step(model, optimizer, criterion, inputs, labels)
    assert isinstance(loss, float)
    assert loss > 0


def test_train_step_updates_weights():
    model = SimpleNetwork()
    criterion = create_loss_function()
    optimizer = create_optimizer(model, learning_rate=0.1)

    inputs = torch.randn(16, 784)
    labels = torch.randint(0, 10, (16,))

    initial_weight = model.fc1.weight.data.clone()
    train_step(model, optimizer, criterion, inputs, labels)
    
    assert not torch.allclose(model.fc1.weight.data, initial_weight)


def test_compute_accuracy_range():
    model = SimpleNetwork()
    inputs = torch.randn(100, 784)
    labels = torch.randint(0, 10, (100,))

    accuracy = compute_accuracy(model, inputs, labels)
    assert 0.0 <= accuracy <= 1.0


def test_compute_accuracy_perfect():
    model = SimpleNetwork()
    inputs = torch.randn(10, 784)
    
    with torch.no_grad():
        outputs = model(inputs)
        labels = torch.argmax(outputs, dim=1)
    
    accuracy = compute_accuracy(model, inputs, labels)
    assert accuracy == 1.0


def test_training_reduces_loss():
    torch.manual_seed(42)
    model = SimpleNetwork()
    criterion = create_loss_function()
    optimizer = create_optimizer(model, learning_rate=0.1)

    inputs = torch.randn(32, 784)
    labels = torch.randint(0, 10, (32,))

    initial_loss = train_step(model, optimizer, criterion, inputs, labels)
    
    for _ in range(10):
        loss = train_step(model, optimizer, criterion, inputs, labels)

    assert loss < initial_loss
