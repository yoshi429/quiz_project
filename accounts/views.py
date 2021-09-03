from accounts.models import Profile
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .forms import UserRegistrationForm, UserLoginForm, ContactUsForm, EditProfileForm
from quizes.models import Quiz


User = get_user_model()


class RegistrationUserView(CreateView):
    template_name = 'accounts/user_register.html'
    # template_name = 'form.html'
    form_class = UserRegistrationForm


class LoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserLoginForm


class LogoutView(LoginRequiredMixin, LogoutView):
    pass


def my_quiz_list(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise ValidationError('このユーザーは存在しません。')
    quizes = Quiz.objects.filter(user=user)
    return render(request, 'accounts/my_quiz_list.html', context={'my_quiz_list':quizes})


class MyQuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'accounts/my_quiz_detail.html'


def post_contact(request, *args, **kwargs):
    form = ContactUsForm(request.POST or None)
    data = {}
    if request.is_ajax():
        if form.is_valid():
            form.save()
            author = form.cleaned_data.get('author')
            data['author'] = author
            return JsonResponse(data)

    context = {
        'form': form
    }
    return render(request, 'accounts/customer_opinion.html', context)


def profile_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
    except:
        raise ValidationError('このユーザーは存在しません。')
    return render(request, 'accounts/profile.html', context={'profile': profile})


@login_required
def edit_profile_view(request, user_id):
    
    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
    except:
        raise ValidationError('このユーザーは存在しません。')
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            data = form.cleaned_data
            introduce = data['introduce']
            profile.introduce = introduce
            profile.save()
            return redirect('user-profile', user_id=user_id) 

    form = EditProfileForm()
    return render(request, 'accounts/edit_profile.html', context={'form': form})


@login_required
def handle_follow(request, user_id):
    me = request.user

    if me.id == user_id:
        return JsonResponse({'message': 'you cannot follow yourself'})

    try:
        other_user = User.objects.get(id=user_id)
    except:
        raise ValidationError('このユーザーは存在しません。')
    other_user_profile = other_user.profile

    if me in other_user.profile.followers.all():
        print('unfollow')
        other_user_profile.followers.remove(me)

    else:
        print('follow')
        other_user_profile.followers.add(me)

    return redirect('user-profile', user_id=user_id) 



def follower_list_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise ValidationError('このユーザーは存在しません。')

    followers = user.profile.followers.all()
    print('follower', followers)
    return render(request, 'accounts/follower_list.html', context={'followers': followers})



def follow_list_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise ValidationError('このユーザーは存在しません。')

    follows = user.following.all()
    print('follow', follows)
    return render(request, 'accounts/follow_list.html', context={'follows': follows})


def my_good_list(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise ValidationError('このユーザーは存在しません。')

    quizes = user.quiz_user.all()
    
    return render(request, 'accounts/my_good_list.html', context={'quizes':quizes})