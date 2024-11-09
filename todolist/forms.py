from django import forms
from .models import Task
from django.core.exceptions import ValidationError


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]


class TaskDetailForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    class Meta:
        model = Task
        fields = ["title", "description", "due_date"]


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "due_date",
            "created_at",
            "completed_at",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "created_at": forms.DateInput(attrs={"type": "date"}),
            "completed_at": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        completed_at = cleaned_data.get("completed_at")

        if status == Task.PENDING and completed_at is not None:
            raise ValidationError("Pending task cannot have a completion date!")

        if status == Task.COMPLETED and completed_at is None:
            raise ValidationError("Completed task must have a completion date!")

        return cleaned_data
