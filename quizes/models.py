from django.db import models
from django.contrib.auth import get_user_model

import random

from django.conf import settings
from django.db.models.deletion import CASCADE

DIFF_CHOICES = settings.DIFF_CHOICES

CATEGORY_CHOICES = settings.CATEGORY_CHOICES

User = get_user_model()


class QuizLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    number_of_questions = models.IntegerField()
    rimit_time = models.IntegerField()
    difficulty = models.CharField(max_length=10, choices=DIFF_CHOICES)
    purpose = models.CharField(max_length=255, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='quiz_user', blank=True, through=QuizLike)

    def __str__(self):
        return f"{self.name}-{self.difficulty}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answer_set.all()

    def get_text_explanation(self):
        return self.quizexpalanation.text
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question.text} - {self.text}'


class QuizExplanation(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField(default='なし')
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}-{self.content}"
