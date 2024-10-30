from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, Value, When
from django.db import models

from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return (
            self.model.objects.filter(assigned_to=self.request.user).annotate(
                priority_order=Case(
                    When(priority='high', then=Value(1)),
                    When(priority='medium', then=Value(2)),
                    When(priority='low', then=Value(3)),
                    output_field=models.IntegerField()
                ),
                status_order=Case(
                    When(status='pending', then=Value(1)),
                    When(status='in_progress', then=Value(1)),
                    When(status='completed', then=Value(2)),
                    output_field=models.IntegerField()
                )
            ).order_by('status_order', 'priority_order', 'due_date', 'title')
        )


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        # Automatically assign task to current user
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        # Only allow the user to modify their own tasks
        return Task.objects.filter(assigned_to=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        # Only allow the user to delete their own tasks
        return Task.objects.filter(assigned_to=self.request.user)