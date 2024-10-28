from django.db import models
from django.conf import settings

from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Task(models.Model):
    ESTATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    due_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='tasks')
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['priority', 'status', 'due_date', 'title']