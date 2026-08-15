"""
Unit tests for the Task API.
Run with: python manage.py test
Or: python -m pytest api/tests.py -v
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task


class TaskModelTest(TestCase):
    """Tests for the Task model."""

    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="todo"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, "todo")

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test Task")

    def test_task_default_status(self):
        task = Task.objects.create(title="New Task")
        self.assertEqual(task.status, "todo")


class TaskAPITest(TestCase):
    """Tests for the Task API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="todo"
        )
        self.list_url = reverse("task-list")
        self.detail_url = reverse("task-detail", kwargs={"pk": self.task.pk})

    def test_get_all_tasks(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        data = {"title": "New Task", "description": "New Description", "status": "todo"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_single_task(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Task")

    def test_update_task(self):
        data = {"title": "Updated Task", "description": "Updated", "status": "done"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_partial_update_task(self):
        response = self.client.patch(self.detail_url, {"status": "in_progress"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "in_progress")

    def test_delete_task(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_filter_by_status(self):
        Task.objects.create(title="Done Task", status="done")
        response = self.client.get("/api/tasks/by_status/?status=done")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_tasks(self):
        Task.objects.create(title="Another Task", description="Searchable content")
        response = self.client.get(self.list_url, {"search": "Searchable"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)