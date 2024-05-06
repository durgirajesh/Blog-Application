from django.urls import path
from posts.views import Posts

urlpatterns = [
    path('', Posts.as_view())    
]