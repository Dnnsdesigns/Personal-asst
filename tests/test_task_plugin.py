"""Unit tests for the task plugin."""

import pytest
from src.plugins.task_plugin import TaskPlugin


@pytest.fixture
def task_plugin():
    """Create a task plugin instance for testing."""
    config = {"enabled": True, "max_tasks": 100}
    return TaskPlugin(config)


def test_add_task(task_plugin):
    """Test adding a task."""
    response = task_plugin.execute("add task buy groceries", {})
    assert "Added task: buy groceries" in response
    assert len(task_plugin.tasks) == 1


def test_list_empty_tasks(task_plugin):
    """Test listing when no tasks exist."""
    response = task_plugin.execute("list tasks", {})
    assert "No tasks found" in response


def test_list_tasks(task_plugin):
    """Test listing tasks."""
    task_plugin.execute("add task buy groceries", {})
    task_plugin.execute("add task walk the dog", {})
    
    response = task_plugin.execute("list tasks", {})
    assert "buy groceries" in response
    assert "walk the dog" in response


def test_complete_task(task_plugin):
    """Test completing a task."""
    task_plugin.execute("add task buy groceries", {})
    response = task_plugin.execute("complete task 1", {})
    
    assert "Completed task: buy groceries" in response
    assert task_plugin.tasks[0]["completed"] is True


def test_can_handle(task_plugin):
    """Test input handling detection."""
    assert task_plugin.can_handle("add task something")
    assert task_plugin.can_handle("I need to remember to do something")
    assert not task_plugin.can_handle("what's the weather like?")