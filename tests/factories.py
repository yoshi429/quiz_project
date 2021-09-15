import factory
from faker import Faker

from django.contrib.auth import get_user_model
from quizes.models import (
    Category, Quiz, QuizExplanation,
    Answer, Question, Comment
)

fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    is_staff = 'True'


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'django'


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    name = fake.name() + " " + "Quiz"
    number_of_questions = 1
    rimit_time = '1'
    difficulty = '初級'
    purpose = 'test'


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
    
    quiz = factory.SubFactory(QuizFactory)
    text = 'factory_quesiton'


class AnswerFactory01(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer 
    
    question = factory.SubFactory(QuestionFactory)
    text = "factory_answer01"
    is_correct = True


class AnswerFactory02(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer 
    
    question = factory.SubFactory(QuestionFactory)
    text = "factory_answer02"
    is_correct = False


class QuizExplanationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuizExplanation

    question = factory.SubFactory(QuestionFactory)
    text = "factory_quizexplanaiton_text"
    source = fake.url()