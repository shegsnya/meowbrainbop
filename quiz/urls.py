from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.list_quizzes, name='list_quizzes'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('quizzes/', views.home, name='quiz_list'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('<int:quiz_id>/results/<int:score>/<int:total>/', views.quiz_results, name='quiz_results'),



]

