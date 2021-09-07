from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from faker import Faker

from accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):
        # fake = Faker('ja_JP')
        fake = Faker()

        for _ in range(10):
            full_name = fake.name()
            first_name = full_name.split()[0]
            email = first_name + "@mail.com"
            password = fake.password()
            user = User.objects.create(username=full_name, email=email)
            validate_password(password, user)
            user.set_password(password)
            user.save()
            Profile.objects.create(user=user)
            print(f"{full_name} ,{email} ,{password}")

        user_accounts  =User.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f"succees create 10 accounts! now you have{user_accounts}accounts!"))
