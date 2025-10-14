from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Task, SubTask, Note, Category, Priority
from .forms import TaskForm, SubTaskForm, NoteForm, CategoryForm, PriorityForm


# 🏠 DASHBOARD VIEW (get_context_data)
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # Dashboard statistics
        context["pending_tasks"] = Task.objects.filter(status="Pending").count()
        context["completed_tasks"] = Task.objects.filter(status="Completed").count()
        context["high_priority_tasks"] = Task.objects.filter(priority__name__icontains="High").count()
        context["due_today_tasks"] = Task.objects.filter(deadline__date=today).count()

        # Recently added tasks
        context["recent_tasks"] = Task.objects.order_by("-created_at")[:5]

        # Totals
        context["total_categories"] = Category.objects.count()
        context["total_priorities"] = Priority.objects.count()
        context["total_notes"] = Note.objects.count()

        return context


# 🧾 TASK VIEWS (get_queryset + get_ordering)
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("category", "priority")
        query = self.request.GET.get("q")

        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
                | Q(priority__name__icontains=query)
            )
        return qs.order_by(self.get_ordering())

    def get_ordering(self):
        allowed = ["title", "deadline", "status", "priority__name", "category__name"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "deadline"


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task-list')


# 🧩 SUBTASK VIEWS (search + sort)
class SubTaskList(ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'subtask_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("parent_task")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(parent_task__title__icontains=query)
            )
        return qs.order_by(self.get_ordering())

    def get_ordering(self):
        allowed = ["title", "status", "parent_task__title"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "title"


class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_confirm_delete.html'
    success_url = reverse_lazy('subtask-list')


# 🗒 NOTE VIEWS (search + sort)
class NoteList(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("task")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(content__icontains=query)
                | Q(task__title__icontains=query)
            )
        return qs.order_by(self.get_ordering())

    def get_ordering(self):
        allowed = ["content", "task__title", "created_at"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "-created_at"


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('note-list')


# 🗂 CATEGORY VIEWS (search + sort)
class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs.order_by(self.get_ordering())

    def get_ordering(self):
        return self.request.GET.get("sort_by", "name")


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category-list')


# 🚩 PRIORITY VIEWS (search + sort)
class PriorityList(ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'priority_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs.order_by(self.get_ordering())

    def get_ordering(self):
        return self.request.GET.get("sort_by", "name")


class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')


class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')


class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'priority_confirm_delete.html'
    success_url = reverse_lazy('priority-list')
