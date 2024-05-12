from django.urls import path
from posts.views import PostHandler, updatePost

urlpatterns = [
    path('', PostHandler.as_view()),
    path('<str:username>', updatePost, name='update_post')    
]