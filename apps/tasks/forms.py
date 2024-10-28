from django import forms
from django.forms.widgets import DateInput

from .models import Category, Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'categories', 'status', 'priority', 'due_date']
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']