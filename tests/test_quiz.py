import pytest


@pytest.fixture
def test_quizmodel():
    from quizes.models import Quiz
    return Quiz


@pytest.mark.django_db
def test_app_is_empty(test_quizmodel):
    count = test_quizmodel.objects.count()
    assert count == 0
    