from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Add-task form. added_by is set in the view from the logged-in
    user's role."""

    class Meta:
        model = Task
        fields = ["description", "is_urgent", "deadline"]
        widgets = {
            "description": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Kya kaam hai...",
                "autofocus": True,
            }),
            "deadline": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        }
        labels = {
            "description": "Task",
            "is_urgent": "Urgent hai",
            "deadline": "Deadline (optional)",
        }


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["added_by", "description", "is_urgent", "deadline"]
        widgets = {
            "added_by": forms.Select(attrs={"class": "form-select"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
        labels = {
            "added_by": "Kaun add kar raha hai",
            "description": "Task",
            "is_urgent": "Urgent hai",
            "deadline": "Deadline",
        }
