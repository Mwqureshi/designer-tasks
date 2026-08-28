from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("task/<int:pk>/pick/", views.pick_task, name="pick_task"),
    path("task/<int:pk>/pause/", views.pause_task, name="pause_task"),
    path("task/<int:pk>/resume/", views.resume_task, name="resume_task"),
    path("task/<int:pk>/release/", views.release_task, name="release_task"),
    path("task/<int:pk>/complete/", views.complete_task, name="complete_task"),
    path("task/<int:pk>/reopen/", views.reopen_task, name="reopen_task"),
    path("task/<int:pk>/delete/", views.delete_task, name="delete_task"),
    path("task/<int:pk>/edit/", views.edit_task, name="edit_task"),
]
