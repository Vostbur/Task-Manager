import random

from django.core.management.base import BaseCommand

from faker import Faker

from backend.models import Project, Task


class Command(BaseCommand):
    help = 'Filling db with test data'

    def generate(self, amount=5):
        fake = Faker('ru_RU')

        for _ in range(amount):
            project = Project.objects.create(
                project_name=fake.text(max_nb_chars=50)
            )
            for _ in range(amount):
                Task.objects.create(
                    project=project,
                    task_name=fake.text(max_nb_chars=50),
                    is_done=random.choice([True, False])
                )

    def handle(self, *args, **options):
        self.generate()
