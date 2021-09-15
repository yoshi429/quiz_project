from pytest_factoryboy import register
from tests.factories import (
    UserFactory, CategoryFactory, QuizFactory,
    QuestionFactory, AnswerFactory01, AnswerFactory02,
    QuizExplanationFactory
    )

register(UserFactory)
register(CategoryFactory)
register(QuizFactory) 
register(QuestionFactory)
register(AnswerFactory01)
register(AnswerFactory02)
register(QuizExplanationFactory)