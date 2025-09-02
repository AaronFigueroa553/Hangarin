from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from todoorg.models import Category, Priority, Task, SubTask, Note

class Command(BaseCommand):
    help = 'Create initial data for the web application'

    def handle(self, *args, **kwargs):
        self.create_task(10)
        self.create_notes(10)
        self.create_subtask(10)

    def create_task(self, count):
        fake = Faker()

        for _ in range(count):
            words = [fake.word() for _ in range(2)]  # two words
            task_name = ' '.join(words)
            Task.objects.create(    
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_between()),
                status=fake.random_element(
                    elements=['Pending', 'In Progress', 'Completed']
                    ),
                category=Category.objects.order_by('?').first(),
                priority=Priority.objects.order_by('?').first(),
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for task created successfully.'))
    
    def create_notes(self, count):
        fake = Faker()

        for _ in range(count):
            words = [fake.word() for _ in range(2)]  # two words
            note_name = ' '.join(words)
            Note.objects.create(    
                task=Task.objects.order_by('?').first(),
                content=fake.paragraph(nb_sentences=3),
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for note created successfully.'))

    def create_subtask(self, count):
        fake = Faker()

        for _ in range(count):
            words = [fake.word() for _ in range(2)]  # two words
            subtask_name = ' '.join(words)
            SubTask.objects.create(    
                parent_task=Task.objects.order_by('?').first(),
                title=fake.sentence(nb_words=5),
                status=fake.random_element(
                    elements=['Pending', 'In Progress', 'Completed']
                    ),
                

            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for subtask created successfully.'))