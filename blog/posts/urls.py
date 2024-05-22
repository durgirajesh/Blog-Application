from django.urls import path
from posts.views import PostCreateHandler, CommentsHandler, PostUpdateHandler

urlpatterns = [
    path('', PostCreateHandler.as_view()),
    path('/<str:username>', PostUpdateHandler.as_view()),
    path('/comments/', CommentsHandler.as_view())      
]