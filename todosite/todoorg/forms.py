from django import forms
from .models import Task, SubTask, Note, Category, Priority

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = '__all__'

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = '__all__'