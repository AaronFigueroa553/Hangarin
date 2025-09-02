from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Priority(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name


class Category(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Task(BaseModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('In progress', 'In Progress'),
            ('Completed', 'Completed'),
        ],
        default='Pending',
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Note(BaseModel):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)

    def __str__(self):
        return self.content
    

class SubTask(BaseModel):
    id = models.AutoField(primary_key=True)
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('In progress', 'In Progress'),
            ('Completed', 'Completed'),
        ],
        default='Pending',
    )

    def __str__(self):
        return self.title
