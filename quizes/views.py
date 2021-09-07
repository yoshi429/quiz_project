from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.generic import ListView

from .models import Quiz, Category, Question, Answer, QuizExplanation, Comment
from .forms import CreateQuizForm, AddQuestionForm, EditQuestionForm, CommentQuizForm


def quiz_play_view(request, pk):
    """
    クイズをする機能
    """
    quiz = Quiz.objects.get(id=pk)
    return render(request, 'quizes/play.html', context={'quiz': quiz})


def question_data(request, pk):
    """
    クイズのデータを送信
    """
    try:
        quiz = Quiz.objects.get(id=pk)
    except:
        raise ValidationError('このクイズは存在しません。')
    question_data = []
    for question in quiz.get_questions():
        answer_list = []
        for answer in question.get_answers():
            answer_list.append(answer.text)
        question_data.append({str(question): answer_list})
    return JsonResponse({'data': question_data, 'time': quiz.rimit_time})


def result_view(request, pk):
    """
    クイズの結果を受信し、結果を返す
    """
    if request.is_ajax():
        questions = []
        results = []
        data = request.POST
        data = dict(data.lists())
        data.pop('csrfmiddlewaretoken')
        try:
            quiz = Quiz.objects.get(id=pk)
        except:
            raise ValidationError('このクイズは存在しません。')
        for question_text in data.keys():
            question = Question.objects.get(text=question_text, quiz=quiz)
            questions.append(question)

        for question in questions:
            your_answer = request.POST.get(question.text)
            question_explaination = QuizExplanation.objects.get(question=question)
            explaination = question_explaination.text
            explaination_source = question_explaination.source
            answers = Answer.objects.filter(question=question)

            for answer in answers:
                if answer.is_correct:
                    correct_answer = answer.text
            if your_answer != "":
                results.append({str(question): {'correct_answer': correct_answer, 'your_answer': your_answer, 'question_expalination': {'expalaination': explaination, 'explaination_source': explaination_source}}})
            else:
                results.append({str(question): {'correct_answer': correct_answer ,'your_answer': '', 'question_expalination': {'expalaination': explaination, 'explaination_source': explaination_source}}})

        return JsonResponse({'results': results})


class QuizListView(ListView):
    """
    クイズ一覧
    """
    context_object_name = 'quiz_list'
    template_name = 'quizes/list.html'
    model = Quiz
    paginate_by = 3

    def get_queryset(self):
        query =  super().get_queryset()
        search_word = self.request.GET.get('search_word', None)
        if search_word:
            query = query.filter(
                Q(category__name__icontains=search_word) | Q(name__icontains=search_word)
                )
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_word'] = self.request.GET.get('search_word', '')
        context['category_list'] = Category.objects.all()
        return context


@login_required
def create_quiz_view(request):
    """
    クイズの投稿機能
    """
    form = CreateQuizForm()
    user = request.user
    if not user.is_authenticated:
        user = None
        raise ValidationError('ログインしてください')

    if request.method == "POST":
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            category_name = data['category_name']
            quiz_title = data['quiz_title']
            rimit_time = data['rimit_time']
            difficulty = data['difficulty']
            purpose = data['purpose']
            question_text = data['question_text']
            answer_choice_1 = data['answer_choice_1']
            answer_choice_2 = data['answer_choice_2']
            answer_choice_3 = data['answer_choice_3']
            answer_choice_4 = data['answer_choice_4']
            correct_answer = data['correct_answer']
            question_expalaination_text = data['question_expalaination_text']
            question_expalaination_source = data['question_expalaination_source']

            category, created = Category.objects.get_or_create(name=category_name)

            quiz = Quiz.objects.create(
                user=user, category=category, name=quiz_title, number_of_questions=1, rimit_time=rimit_time, difficulty=difficulty, purpose=purpose)
            
            question = Question.objects.create(quiz=quiz, text=question_text)
            
            Answer.objects.create(question=question, text=answer_choice_1, is_correct= True if answer_choice_1 == correct_answer else False)
            Answer.objects.create(question=question, text=answer_choice_2, is_correct= True if answer_choice_2 == correct_answer else False)
            Answer.objects.create(question=question, text=answer_choice_3, is_correct= True if answer_choice_3 == correct_answer else False)
            Answer.objects.create(question=question, text=answer_choice_4, is_correct= True if answer_choice_4 == correct_answer else False)

            QuizExplanation.objects.create(question=question, text=question_expalaination_text, source=question_expalaination_source)

            return redirect('list')

    return render(request, 'components/create_add_edit_question.html', {'form': form})


@login_required
def add_question_view(request, pk):
    """
    既存のクイズに問題を追加する機能
    """
    form = AddQuestionForm()
    user = request.user

    try:
        quiz = Quiz.objects.get(id=pk, user=user)
    except Quiz.DoesNotExist:
        raise Http404('このクイズは存在しません。')
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rimit_time = data['rimit_time']
            question_text = data['question_text']
            answer_choice_1 = data['answer_choice_1']
            answer_choice_2 = data['answer_choice_2']
            answer_choice_3 = data['answer_choice_3']
            answer_choice_4 = data['answer_choice_4']
            correct_answer = data['correct_answer']
            question_expalaination_text = data['question_expalaination_text']
            question_expalaination_source = data['question_expalaination_source']

            quiz.rimit_time = rimit_time
            quiz.number_of_questions = quiz.number_of_questions + 1
            quiz.save()
            question = Question.objects.create(quiz=quiz, text=question_text)

            Answer.objects.create(question=question, text=answer_choice_1, is_correct= True if answer_choice_1 == correct_answer else False)
            Answer.objects.create(question=question, text=answer_choice_2, is_correct= True if answer_choice_2 == correct_answer else False)
            Answer.objects.create(question=question, text=answer_choice_3, is_correct= True if answer_choice_3 == correct_answer else False)
            Answer.objects.create(question=question, text=answer_choice_4, is_correct= True if answer_choice_4 == correct_answer else False)
            
            QuizExplanation.objects.create(question=question, text=question_expalaination_text, source=question_expalaination_source)

            return redirect('my-quiz-list', user_id=user.id)
            
    return render(request, 'components/create_add_edit_question.html', {'form': form})
    

@login_required
def delete_quiz_view(request, pk):
    """
    クイズの削除機能
    """
    user = request.user
    try:
        quiz = Quiz.objects.get(user=user, pk=pk)
    except Quiz.DoesNotExist:
        raise Http404
    quiz.delete()
    return redirect('my-quiz-list', user_id=user.id)
    

@login_required
def delete_question_view(request, pk):
    """
    既存のクイズに存在する問題を削除
    """
    user = request.user
    try:
        question = Question.objects.get(pk=pk)
        quiz = question.quiz
    except Quiz.DoesNotExist:
        raise Http404
    
    if user != quiz.user:
        raise Http404
    
    number_of_questions = quiz.number_of_questions
    quiz.number_of_questions = number_of_questions - 1 
    quiz.save()
    
    if quiz.number_of_questions == 0:
        quiz.delete()
    else:
        question.delete()

    return redirect('my-quiz-list', user_id=user.id)


@login_required
def edit_question_view(request, pk):
    """
    既存のクイズの問題を編集する機能
    """
    user = request.user
    form = EditQuestionForm()
    try:
        question = Question.objects.get(pk=pk)
        quiz = question.quiz
        answers = Answer.objects.filter(question=question)
        quiz_explanatioin = QuizExplanation.objects.get(question=question)
    except Quiz.DoesNotExist:
        raise Http404
    
    if user != quiz.user:
        raise Http404
    
    if request.method == 'POST':
        form = EditQuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            question_text = data['question_text']
            answer_choice_1 = data['answer_choice_1']
            answer_choice_2 = data['answer_choice_2']
            answer_choice_3 = data['answer_choice_3']
            answer_choice_4 = data['answer_choice_4']
            correct_answer = data['correct_answer']
            question_expalaination_text = data['question_expalaination_text']
            question_expalaination_source = data['question_expalaination_source']

            
            question.text = question_text
            question.save()

            answer_choice_list = [answer_choice_1, answer_choice_2, answer_choice_3, answer_choice_4]
            
            for i, answer in enumerate(answers):
                answer.text = answer_choice_list[i]
                if answer.text == correct_answer:
                    answer.is_correct = True
                    print('true')
                else:
                    answer.is_correct = False
                answer.save()

            quiz_explanatioin.text = question_expalaination_text
            quiz_explanatioin.source = question_expalaination_source
            quiz_explanatioin.save()
            return redirect('my-quiz-list', user_id=user.id)

    return render(request, 'components/create_add_edit_question.html', {'form': form})


@login_required
def comment_quiz_view(request, quiz_id):
    """
    クイズにコメントする機能
    """
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404
    
    form = CommentQuizForm(request.POST or None)
    
    if form.is_valid():
        data = form.cleaned_data
        content = data['content']
        Comment.objects.create(user=request.user, quiz=quiz, content=content)
        return redirect('comment', quiz_id=quiz_id)

    else:
        comments = Comment.objects.filter(quiz=quiz).all()
        return render(request, 'quizes/comment.html', context={'comments': comments, 'form': form}) 


@login_required
def quiz_handle_like(request, quiz_id):
    """
    クイズのいいね機能
    """
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404
    user = request.user

    if user in quiz.likes.all():
        quiz.likes.remove(user)
        print('unGood')
    else:
        print('Good')
        quiz.likes.add(user)
    return redirect('list')

