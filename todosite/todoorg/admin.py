from django.contrib import admin
from .models import Category, Priority, Task, SubTask, Note

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ("title", "status")
    show_change_link = True
class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    fields = ("content", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "deadline", "priority", "category", )
    search_fields = ("title", "description",)
    list_filter = ("status","priority","category",)

    inlines = [SubTaskInline, NoteInline]

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title","status", "parent_task",)
    search_fields = ("title",)
    list_filter = ("status",)

    def get_member_program(self, obj):
        try:
            member = SubTask.objects.get(id=obj.parent_task_id)
            return member.title  #need fixing
        except title.DoesNotExist:
            return None

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task","content","created_at",)
    search_fields = ("content",)
    list_filter = ("created_at",)
