import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

# use UserFactory
@pytest.mark.django_db
def test_new_user(user_factory):
    user = user_factory.build()
    count = User.objects.all().count()
    print("count", count)
    print("username", user.username)
    assert True