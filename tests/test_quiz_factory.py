import pytest



@pytest.mark.django_db
def test_new_quiz(quiz_factory):
    quiz = quiz_factory.build()
    print(quiz.name)
    assert True


@pytest.mark.django_db
def test_new_question(question_factory):
    question = question_factory.build()
    print(question.text)
    assert question.text == 'factory_quesiton'


@pytest.mark.django_db
def test_new_answer01(answer_factory01):
    answer = answer_factory01.build()
    print(answer.text)
    assert answer.text == "factory_answer01"
    assert answer.is_correct == True


@pytest.mark.django_db
def test_new_answer02(answer_factory02):
    answer = answer_factory02.build()
    print(answer.text)
    assert answer.text == "factory_answer02"
    assert answer.is_correct == False


@pytest.mark.django_db
def test_new_question(quiz_explanation_factory):
    quiz_explaination = quiz_explanation_factory.build()
    print(quiz_explaination.text)
    print(quiz_explaination.source)
    assert quiz_explaination.text == "factory_quizexplanaiton_text"