from django.db import models
from django.utils import timezone

# Fixed mapping of login usernames to their role.
# "waleed" is the manager/admin: full control (add, edit, delete),
# does not pick tasks. "adnan", "hamid", "zain" are designers who
# add and pick tasks from the shared pool.
USER_ROLES = {
    "waleed": {"label": "Waleed", "slug": "waleed", "is_admin": True, "is_designer": False},
    "adnan": {"label": "Adnan", "slug": "adnan", "is_admin": False, "is_designer": True},
    "hamid": {"label": "Hamid", "slug": "hamid", "is_admin": False, "is_designer": True},
    "zain": {"label": "Zain", "slug": "zain", "is_admin": False, "is_designer": True},
}

DESIGNER_USERNAMES = ["adnan", "hamid", "zain"]


def role_for(user):
    """Return the role dict for a logged-in user, or None if unknown."""
    if not user or not user.is_authenticated:
        return None
    return USER_ROLES.get(user.username)


class Task(models.Model):
    ADDED_BY_CHOICES = [
        ("waleed", "Waleed"),
        ("adnan", "Adnan"),
        ("hamid", "Hamid"),
        ("zain", "Zain"),
    ]
    ASSIGNED_CHOICES = [
        ("adnan", "Adnan"),
        ("hamid", "Hamid"),
        ("zain", "Zain"),
    ]
    STATUS_CHOICES = [
        ("available", "Available"),
        ("active", "Active"),
        ("paused", "Paused"),
        ("done", "Done"),
    ]

    description = models.CharField(max_length=500)
    is_urgent = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    added_by = models.CharField(max_length=20, choices=ADDED_BY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    assigned_to = models.CharField(max_length=20, choices=ASSIGNED_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-is_urgent", "deadline", "created_at"]

    def __str__(self):
        return f"[{self.get_added_by_display()}] {self.description}"

    def pick_for(self, designer_slug):
        # Pause whatever this designer currently has active.
        Task.objects.filter(
            assigned_to=designer_slug, status="active"
        ).exclude(pk=self.pk).update(status="paused")
        self.assigned_to = designer_slug
        self.status = "active"
        if not self.started_at:
            self.started_at = timezone.now()
        self.save()

    def pause(self):
        self.status = "paused"
        self.save()

    def resume(self):
        Task.objects.filter(
            assigned_to=self.assigned_to, status="active"
        ).exclude(pk=self.pk).update(status="paused")
        self.status = "active"
        self.save()

    def release(self):
        self.assigned_to = None
        self.status = "available"
        self.save()

    def complete(self):
        self.status = "done"
        self.completed_at = timezone.now()
        self.save()

    def reopen(self):
        self.status = "available"
        self.assigned_to = None
        self.completed_at = None
        self.save()
