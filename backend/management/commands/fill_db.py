import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from faker import Faker

from backend.models import Project, Task


class Command(BaseCommand):
    help = 'Filling db with test data. Username: test_user, password: yjdsq_gfhjkm'

    def generate(self, amount=5):
        fake = Faker('ru_RU')
        try:
            User = get_user_model()
            user = User.objects.create_user(username='test_user', password='yjdsq_gfhjkm')
            user.is_superuser = False
            user.is_staff = False
            user.save()
        except IntegrityError:
            print('Test user is already exists. Username: test_user, password: yjdsq_gfhjkm')
            return

        for _ in range(amount):
            project = Project.objects.create(
                project_name=fake.text(max_nb_chars=50),
                user=user
            )
            for _ in range(amount):
                Task.objects.create(
                    project=project,
                    task_name=fake.text(max_nb_chars=50),
                    is_done=random.choice([True, False])
                )

    def handle(self, *args, **options):
        self.generate()
        print('Database is filled with test data. Username: test_user, password: yjdsq_gfhjkm')
