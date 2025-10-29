"""Example task management plugin."""

import re
from typing import Dict, Any, List
from datetime import datetime

from src.core.plugin_base import BasePlugin


class TaskPlugin(BasePlugin):
    """Plugin for managing personal tasks."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the task plugin."""
        super().__init__(config)
        self.tasks: List[Dict[str, Any]] = []

    def get_capabilities(self) -> Dict[str, Any]:
        """Return plugin capabilities."""
        return {
            "name": "Task Management",
            "description": "Manage personal tasks and to-do items",
            "commands": self.get_commands(),
            "version": "1.0.0"
        }

    def get_commands(self) -> List[str]:
        """Get supported commands."""
        return [
            "add task [description]",
            "list tasks",
            "complete task [id]",
            "remove task [id]"
        ]

    def can_handle(self, user_input: str) -> bool:
        """Check if this plugin can handle the input."""
        keywords = ["task", "todo", "to-do", "remind", "remember"]
        return any(keyword in user_input.lower() for keyword in keywords)

    def execute(self, user_input: str, context: Dict[str, Any]) -> str:
        """Execute task management functionality."""
        input_lower = user_input.lower()

        if "add" in input_lower and "task" in input_lower:
            return self._add_task(user_input)
        elif "list" in input_lower and "task" in input_lower:
            return self._list_tasks()
        elif "complete" in input_lower and "task" in input_lower:
            return self._complete_task(user_input)
        elif "remove" in input_lower and "task" in input_lower:
            return self._remove_task(user_input)
        else:
            return self._general_task_help()

    def _add_task(self, user_input: str) -> str:
        """Add a new task."""
        # Extract task description
        match = re.search(r'add task (.+)', user_input, re.IGNORECASE)
        if not match:
            return "Please provide a task description. Example: 'add task buy groceries'"

        description = match.group(1).strip()
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        
        self.tasks.append(task)
        return f"✅ Added task: {description}"

    def _list_tasks(self) -> str:
        """List all tasks."""
        if not self.tasks:
            return "📝 No tasks found. Add a task with 'add task [description]'"

        active_tasks = [t for t in self.tasks if not t["completed"]]
        completed_tasks = [t for t in self.tasks if t["completed"]]

        response = "📝 **Your Tasks:**\n\n"
        
        if active_tasks:
            response += "**Active Tasks:**\n"
            for task in active_tasks:
                response += f"  {task['id']}. {task['description']}\n"
            response += "\n"

        if completed_tasks:
            response += "**Completed Tasks:**\n"
            for task in completed_tasks:
                response += f"  ✓ {task['id']}. {task['description']}\n"

        return response

    def _complete_task(self, user_input: str) -> str:
        """Mark a task as completed."""
        match = re.search(r'complete task (\d+)', user_input, re.IGNORECASE)
        if not match:
            return "Please specify a task ID. Example: 'complete task 1'"

        task_id = int(match.group(1))
        task = self._find_task(task_id)
        
        if not task:
            return f"❌ Task {task_id} not found"

        if task["completed"]:
            return f"✅ Task {task_id} is already completed"

        task["completed"] = True
        task["completed_at"] = datetime.now().isoformat()
        return f"✅ Completed task: {task['description']}"

    def _remove_task(self, user_input: str) -> str:
        """Remove a task."""
        match = re.search(r'remove task (\d+)', user_input, re.IGNORECASE)
        if not match:
            return "Please specify a task ID. Example: 'remove task 1'"

        task_id = int(match.group(1))
        task = self._find_task(task_id)
        
        if not task:
            return f"❌ Task {task_id} not found"

        self.tasks.remove(task)
        return f"🗑️ Removed task: {task['description']}"

    def _find_task(self, task_id: int) -> Dict[str, Any]:
        """Find a task by ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def _general_task_help(self) -> str:
        """Provide general help for task management."""
        return ("I can help you manage tasks! Try:\n"
                "• 'add task [description]' - Add a new task\n"
                "• 'list tasks' - Show all tasks\n"
                "• 'complete task [id]' - Mark task as done\n"
                "• 'remove task [id]' - Delete a task")