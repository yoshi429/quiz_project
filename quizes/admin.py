from django.contrib import admin

# Register your models here.

from .models import Category, Quiz, Question, Answer, QuizExplanation, Comment

class QuizInline(admin.TabularInline):
    model = Quiz

class CategoryAdmin(admin.ModelAdmin):
    inlines = [QuizInline]



admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz)


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(QuizExplanation)
admin.site.register(Comment)