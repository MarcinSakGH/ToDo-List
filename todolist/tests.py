from django.test import TestCase
from .models import Task
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your tests here.


class TaskModelTest(TestCase):
    def setUp(self):
        """Create user and a task for tests"""
        self.user = get_user_model().objects.create(
            username="testuser",
            password="testpassword"
            )
        self.task = Task.objects.create(
            title="Test Task",
            description="Test description",
            user=self.user
            )

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
        # check if completed at is not in the future
        self.assertTrue(self.task.completed_at <= timezone.now().date())