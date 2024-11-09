from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.test.client import Client
from .models import Task


# Create your tests here.


def create_user_and_task():
    """Helper function to create user and task for tests"""
    user = get_user_model().objects.create_user(
        username="testuser", password="testpassword-123"
    )
    task = Task.objects.create(
        title="Test Task", description="Test description", user=user
    )
    return user, task


class TaskModelTest(TestCase):

    def setUp(self):
        """Create user and a task for tests"""
        self.user, self.task = create_user_and_task()

    def test_task_creation(self):
        """Test if task is created correctly"""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test description")
        self.assertEqual(self.task.status, Task.PENDING)
        self.assertIsNone(self.task.completed_at)
        self.assertIsNotNone(self.task.created_at)

    def test_mark_as_completed_method(self):
        """Test if mark_as_completed method works correctly"""
        self.task.mark_as_completed()
        self.assertEqual(self.task.status, Task.COMPLETED)
        self.assertIsNotNone(self.task.completed_at)
        self.assertTrue(self.task.completed_at <= timezone.now().date())


class TestViews(TestCase):
    def setUp(self):
        self.user, self.task = create_user_and_task()

    def test_task_list_view(self):
        """Test TaskListView"""
        print("username", self.user.username)
        print("is pass ok:", self.user.check_password("testpassword-123"))
        login_successful = self.client.login(
            username="testuser", password="testpassword-123"
        )
        print(f"Login successful: {login_successful}")

        url = reverse("task_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_list.html")
