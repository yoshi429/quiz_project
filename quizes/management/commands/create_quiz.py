import random

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker
import faker.providers

from quizes.models import (
    Category, Quiz, QuizExplanation, 
    Question, Answer 
) 

User = get_user_model()

DIFF_CHOICES = settings.DIFF_CHOICES


class QuizProvider(faker.providers.BaseProvider):
    def quiz_category(self):
        categories = Category.objects.all()
        return self.random_element(categories)
    
    def quiz_difficulty(self):
        return self.random_element(DIFF_CHOICES)[0]

    def random_user(self):
        users = User.objects.all()
        return self.random_element(users)


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):
        fake = Faker('ja_JP')
        fake.add_provider(QuizProvider)
        
        for _ in range(5):
            user = fake.unique.random_user()
            category = fake.unique.quiz_category()
            name = fake.text(max_nb_chars=15)
            rimit_time = random.randint(1, 10)
            difficulty = fake.quiz_difficulty()
            number_of_questions = 1
            purpose = fake.text(max_nb_chars=20)
            question_text = fake.text(max_nb_chars=30)
            answer_1_text = fake.unique.text(max_nb_chars=10)
            answer_2_text = fake.unique.text(max_nb_chars=10)
            answer_3_text = fake.unique.text(max_nb_chars=10)
            answer_4_text = fake.unique.text(max_nb_chars=10)
            correct_answer_text = random.choice([answer_1_text, answer_2_text, answer_3_text, answer_4_text])
            quiz_explanation_text =  fake.text(max_nb_chars=20)
            quiz_explanation_souce = fake.url()
            quiz = Quiz.objects.create(
                                        user=user, 
                                        category=category, 
                                        name=name, 
                                        number_of_questions=number_of_questions, 
                                        rimit_time=rimit_time,
                                        difficulty=difficulty,
                                        purpose=purpose
                                        )
            question = Question.objects.create(quiz=quiz, text=question_text)
            Answer.objects.create(question=question, text=answer_1_text, is_correct= True if answer_1_text == correct_answer_text else False)
            Answer.objects.create(question=question, text=answer_2_text, is_correct= True if answer_2_text == correct_answer_text else False)
            Answer.objects.create(question=question, text=answer_3_text, is_correct= True if answer_3_text == correct_answer_text else False)
            Answer.objects.create(question=question, text=answer_4_text, is_correct= True if answer_4_text == correct_answer_text else False)
            
            QuizExplanation.objects.create(question=question, text=quiz_explanation_text, source=quiz_explanation_souce)
        
        quizes_counts = Quiz.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f"Success create 10 quizes! Now you have {quizes_counts} quizes"))
            
            

