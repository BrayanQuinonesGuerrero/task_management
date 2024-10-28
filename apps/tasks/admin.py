from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Category, Task


class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']


class TaskAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'title', 'priority', 'status', 'due_date', 'assigned_to']
    list_filter = ['priority', 'status', 'due_date', 'assigned_to']
    search_fields = ['title', 'priority', 'status']
    ordering = ['priority', 'status', 'due_date', 'title']
    autocomplete_fields = ['assigned_to']


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)