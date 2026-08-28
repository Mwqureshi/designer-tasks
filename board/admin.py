from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("description", "added_by", "status", "assigned_to", "is_urgent", "deadline", "created_at")
    list_filter = ("status", "assigned_to", "is_urgent")
    search_fields = ("description",)
