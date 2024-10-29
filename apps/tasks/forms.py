from django import forms
from django.forms.widgets import DateInput

from .models import Category, Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'categories', 'status', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']