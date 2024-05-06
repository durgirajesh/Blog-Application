from django.urls import path
from posts.views import Posts

urlpatterns = [
    path('', Posts.as_view(), name='create_post'), 
    path('', Posts.as_view(), name='update_post')   
]