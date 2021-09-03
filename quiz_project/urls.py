"""quiz_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from allauth.socialaccount.providers.google.urls import urlpatterns as google_url


from frontend.views import (
    HomeView,  terms_of_service_view, page_not_found, server_error
    )

from quizes.views import (
    QuizListView, quiz_play_view, question_data, 
    result_view, create_quiz_view, add_question_view, 
    delete_quiz_view, delete_question_view, edit_question_view,
    comment_quiz_view, quiz_handle_like, 
    )

from accounts.views import (
    RegistrationUserView, LoginView, LogoutView,
    my_quiz_list, MyQuizDetailView, post_contact,
    edit_profile_view, profile_view, handle_follow,
    follower_list_view, follow_list_view, my_good_list,
    )



urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth_accounts/', include(google_url)),
    
    path('home/', HomeView.as_view(), name='home'),
    path('contact-us/', post_contact, name='post_contact_us' ),
    path('terms_of_service/', terms_of_service_view, name='terms_of_service' ),

    path('', QuizListView.as_view(), name='list'),
    path('<int:pk>/', quiz_play_view, name='play'),
    path('<int:pk>/data/', question_data, name='data'),
    path('<int:pk>/result/', result_view, name='result'),
    path('<int:quiz_id>/comment/', comment_quiz_view, name='comment'),
    path('<int:quiz_id>/good/', quiz_handle_like, name='quiz-handle-good'),
    path('create/', create_quiz_view, name='create-quiz'),
    path('add-questions/<int:pk>', add_question_view, name='add-question'),
    path('my-quiz-list/<int:user_id>', my_quiz_list, name='my-quiz-list'),
    path('my-quiz-list/delete/<int:pk>', delete_quiz_view, name='quiz-delte'),
    path('quiz-detail/<int:pk>', MyQuizDetailView.as_view(), name='quiz-detail'),
    path('quesiton-detail/<int:pk>/delete', delete_question_view, name='question-delete'),
    path('quesiton-detail/<int:pk>/edit', edit_question_view, name='question-edit'),

    path('user-register/', RegistrationUserView.as_view(), name='user-register'),
    path('user-login/', LoginView.as_view(), name='user-login'),
    path('user-logout/', LogoutView.as_view(), name='user-logout'),
    path('user-profile/<int:user_id>/', profile_view, name='user-profile'),
    path('user-profile/<int:user_id>/edit', edit_profile_view, name='user-profile-edit'),
    path('user-handle-follow/<int:user_id>', handle_follow, name='user-handle-follow'),
    path('user-follower-list/<int:user_id>', follower_list_view, name='follower-list'),
    path('user-follow-list/<int:user_id>', follow_list_view, name='follow-list'),
    path('user/<int:user_id>/good_list', my_good_list, name='good-list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = page_not_found
handler500 = server_error