from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('conversation/', views.conversation, name='conversation'),
    path('games/', views.games, name='games'),
    path('games/vocab/', views.game_vocab_match, name='game_vocab_match'),
    path('games/blanks/', views.game_fill_blanks, name='game_fill_blanks'),
    path('games/memory/', views.game_memory, name='game_memory'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('analysis/', views.analysis, name='analysis'),
    path('api/chat/', views.api_chat, name='api_chat'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
