from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Task, role_for, DESIGNER_USERNAMES, USER_ROLES
from .forms import TaskForm, TaskEditForm


def _redirect_target(request, fallback="task_list"):
    next_url = request.POST.get("next")
    if next_url and next_url.startswith("/"):
        return redirect(next_url)
    return redirect(fallback)


@login_required
def task_list(request):
    role = role_for(request.user)
    if role is None:
        return HttpResponseForbidden("Aapko is app ka access nahin hai.")

    is_admin = bool(role.get("is_admin"))
    is_designer = bool(role.get("is_designer"))
    my_slug = role.get("slug") if is_designer else None

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.added_by = role["slug"]
            task.save()
            messages.success(request, "Task add ho gaya.")
            return redirect("task_list")
    else:
        form = TaskForm()

    pool = Task.objects.filter(status="available")
    done_recent = Task.objects.filter(status="done").order_by("-completed_at")[:20]

    my_active = None
    my_paused = None
    if is_designer:
        my_active = Task.objects.filter(assigned_to=my_slug, status="active").first()
        my_paused = Task.objects.filter(assigned_to=my_slug, status="paused")

    overview = None
    if is_admin:
        overview = []
        for uname in DESIGNER_USERNAMES:
            r = USER_ROLES[uname]
            active = Task.objects.filter(assigned_to=r["slug"], status="active").first()
            paused_count = Task.objects.filter(assigned_to=r["slug"], status="paused").count()
            overview.append({"label": r["label"], "active": active, "paused_count": paused_count})

    context = {
        "form": form,
        "role_label": role["label"],
        "is_admin": is_admin,
        "is_designer": is_designer,
        "my_active": my_active,
        "my_paused": my_paused,
        "pool": pool,
        "pool_total": pool.count(),
        "done_recent": done_recent,
        "overview": overview,
    }
    return render(request, "board/task_list.html", context)


@login_required
def pick_task(request, pk):
    role = role_for(request.user)
    if not (role and role.get("is_designer")):
        return HttpResponseForbidden("Sirf designers task pick kar saktay hain.")
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        if task.status != "available":
            messages.info(request, "Ye task pehle hi kisi ne le liya hai.")
        else:
            task.pick_for(role["slug"])
    return _redirect_target(request)


@login_required
def pause_task(request, pk):
    role = role_for(request.user)
    task = get_object_or_404(Task, pk=pk)
    if not (role and role.get("is_designer") and task.assigned_to == role.get("slug")):
        return HttpResponseForbidden("Aapko ye action karne ki ijazat nahin.")
    if request.method == "POST" and task.status == "active":
        task.pause()
    return _redirect_target(request)


@login_required
def resume_task(request, pk):
    role = role_for(request.user)
    task = get_object_or_404(Task, pk=pk)
    if not (role and role.get("is_designer") and task.assigned_to == role.get("slug")):
        return HttpResponseForbidden("Aapko ye action karne ki ijazat nahin.")
    if request.method == "POST" and task.status == "paused":
        task.resume()
    return _redirect_target(request)


@login_required
def release_task(request, pk):
    role = role_for(request.user)
    task = get_object_or_404(Task, pk=pk)
    if not (role and role.get("is_designer") and task.assigned_to == role.get("slug")):
        return HttpResponseForbidden("Aapko ye action karne ki ijazat nahin.")
    if request.method == "POST" and task.status in ("active", "paused"):
        task.release()
        messages.info(request, "Task wapis pool mein chala gaya.")
    return _redirect_target(request)


@login_required
def complete_task(request, pk):
    role = role_for(request.user)
    task = get_object_or_404(Task, pk=pk)
    if not (role and role.get("is_designer") and task.assigned_to == role.get("slug")):
        return HttpResponseForbidden("Aapko ye action karne ki ijazat nahin.")
    if request.method == "POST" and task.status in ("active", "paused"):
        task.complete()
        messages.success(request, "Task complete ho gaya.")
    return _redirect_target(request)


@login_required
def reopen_task(request, pk):
    role = role_for(request.user)
    is_admin = bool(role and role.get("is_admin"))
    if not is_admin:
        return HttpResponseForbidden("Sirf Waleed hi task reopen kar sakta hai.")
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.reopen()
    return _redirect_target(request)


@login_required
def delete_task(request, pk):
    role = role_for(request.user)
    is_admin = bool(role and role.get("is_admin"))
    if not is_admin:
        return HttpResponseForbidden("Sirf Waleed hi task delete kar sakta hai.")
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        messages.info(request, "Task hata diya gaya.")
    return _redirect_target(request)


@login_required
def edit_task(request, pk):
    role = role_for(request.user)
    is_admin = bool(role and role.get("is_admin"))
    if not is_admin:
        return HttpResponseForbidden("Sirf Waleed hi task edit kar sakta hai.")
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task update ho gaya.")
            return redirect("task_list")
    else:
        form = TaskEditForm(instance=task)
    return render(request, "board/edit_task.html", {"form": form, "task": task})
