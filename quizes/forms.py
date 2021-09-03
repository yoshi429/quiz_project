from quizes.models import Question
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Question


DIFF_CHOICES = settings.DIFF_CHOICES
CATEGORY_CHOICES = settings.CATEGORY_CHOICES


class CreateQuizForm(forms.Form):
    category_name = forms.ChoiceField(label='カテゴリー', choices=CATEGORY_CHOICES)
    quiz_title = forms.CharField(label='タイトル')
    rimit_time = forms.IntegerField(label='制限時間')
    difficulty = forms.ChoiceField(label='難易度', choices=DIFF_CHOICES)
    purpose = forms.CharField(label='目的')
    question_text = forms.CharField(label='問題文')
    answer_choice_1 = forms.CharField(label='選択肢1')
    answer_choice_2 = forms.CharField(label='選択肢2')
    answer_choice_3 = forms.CharField(label='選択肢3')
    answer_choice_4 = forms.CharField(label='選択肢4')
    correct_answer = forms.CharField(label='答え')
    question_expalaination_text = forms.CharField(label='解説')
    question_expalaination_source = forms.CharField(label='ソース')

    def clean(self):
        data = super().clean()
        answer_choice_1 =  data['answer_choice_1']
        answer_choice_2 =  data['answer_choice_2']
        answer_choice_3 =  data['answer_choice_3']
        answer_choice_4 =  data['answer_choice_4']        
        correct_answer =  data['correct_answer']

        if correct_answer != answer_choice_1:
            if correct_answer != answer_choice_2:
                if correct_answer != answer_choice_3:
                    if correct_answer != answer_choice_4:
                        raise ValidationError('選択肢の中に答えがありません。')
        return data
    
    def clean_rimit_time(self):
        rimit_time = self.cleaned_data['rimit_time']
        if rimit_time <=0 or rimit_time > 100:
            raise ValidationError('1から99の間にしてください')
        return rimit_time 
    
    def clean_question_text(self):
        question_text = self.cleaned_data['question_text']
        qs = Question.objects.filter(text=question_text)
        if qs.exists():
            raise ValidationError('この問題は既に存在しています。恐れ入りますが、文章を少し変えてください。')
        return question_text
    

class AddQuestionForm(forms.Form):
    rimit_time = forms.IntegerField(label='制限時間')
    question_text = forms.CharField(label='問題文')
    answer_choice_1 = forms.CharField(label='選択肢1')
    answer_choice_2 = forms.CharField(label='選択肢2')
    answer_choice_3 = forms.CharField(label='選択肢3')
    answer_choice_4 = forms.CharField(label='選択肢4')
    correct_answer = forms.CharField(label='答え')
    question_expalaination_text = forms.CharField(label='解説')
    question_expalaination_source = forms.CharField(label='ソース')

    def clean(self):
        data = super().clean()
        answer_choice_1 =  data['answer_choice_1']
        answer_choice_2 =  data['answer_choice_2']
        answer_choice_3 =  data['answer_choice_3']
        answer_choice_4 =  data['answer_choice_4']
        correct_answer =  data['correct_answer']

        if correct_answer != answer_choice_1:
            if correct_answer != answer_choice_2:
                if correct_answer != answer_choice_3:
                    if correct_answer != answer_choice_4:
                        raise ValidationError('選択肢の中に答えがありません。')
        return data
    
    def clean_rimit_time(self):
        rimit_time = self.cleaned_data['rimit_time']
        if rimit_time <=0 or rimit_time > 100:
            raise ValidationError('1から99の間にしてください')
        return rimit_time 

    def clean_question_text(self):
        question_text = self.cleaned_data['question_text']
        qs = Question.objects.filter(text=question_text)
        if qs.exists():
            raise ValidationError('この問題は既に存在しています。恐れ入りますが、文章を少し変えてください。')
        return question_text


class EditQuestionForm(forms.Form):
    question_text = forms.CharField(label='問題文')
    answer_choice_1 = forms.CharField(label='選択肢1')
    answer_choice_2 = forms.CharField(label='選択肢2')
    answer_choice_3 = forms.CharField(label='選択肢3')
    answer_choice_4 = forms.CharField(label='選択肢4')
    correct_answer = forms.CharField(label='答え')
    question_expalaination_text = forms.CharField(label='解説')
    question_expalaination_source = forms.CharField(label='ソース')

    def clean(self):
        data = super().clean()
        answer_choice_1 =  data['answer_choice_1']
        answer_choice_2 =  data['answer_choice_2']
        answer_choice_3 =  data['answer_choice_3']
        answer_choice_4 =  data['answer_choice_4']
        correct_answer =  data['correct_answer']

        if correct_answer != answer_choice_1:
            if correct_answer != answer_choice_2:
                if correct_answer != answer_choice_3:
                    if correct_answer != answer_choice_4:
                        raise ValidationError('選択肢の中に答えがありません。')
        return data
    
    def clean_rimit_time(self):
        rimit_time = self.cleaned_data['rimit_time']
        if rimit_time <=0 or rimit_time > 100:
            raise ValidationError('1から99の間にしてください')
        return rimit_time 

    def clean_question_text(self):
        question_text = self.cleaned_data['question_text']
        qs = Question.objects.filter(text=question_text)
        if qs.exists():
            raise ValidationError('この問題は既に存在しています。恐れ入りますが、文章を少し変えてください。')
        return question_text


class CommentQuizForm(forms.Form):
    content = forms.CharField(label='コメント')

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) > 255:
            raise ValidationError('255文字以下にしてください')
        return content