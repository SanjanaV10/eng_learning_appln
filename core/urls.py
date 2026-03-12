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
    path('api/assemblyai-token/', views.get_assemblyai_token, name='assemblyai_token'),
    path('api/get-quiz/', views.get_quiz_data, name='get_quiz_data'),
    path('api/get-game/<str:category>/', views.get_game_data, name='get_game_data'),
    path('api/mark-seen/', views.mark_question_seen, name='mark_question_seen'),
    path('api/delete-history/<int:item_id>/', views.delete_history_item, name='delete_history_item'),
    path('api/clear-history/', views.clear_history, name='clear_history'),
    path('history/', views.search_history, name='search_history'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
