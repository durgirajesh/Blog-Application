import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PostModel 
from django.views.generic import View
from django.utils.decorators import method_decorator
from users.models import UserModel
from users.views import isAuthenticated

@method_decorator(csrf_exempt, name='dispatch')
class PostHandler(View):
    def post(self, request):
        response = {}
        post_data = json.loads(request.body.decode('utf-8'))

        if post_data is not None:
            username = post_data.get('username')
            user = UserModel.objects.filter(username=username).first() 
            if user is not None:
                if isAuthenticated(request, username):
                    post_title = post_data.get('title')
                    post = PostModel.objects.filter(author = user, title=post_title).first()

                    if post is not None:
                        response['message'] = 'Post already exists'
                        response['title'] = post.title
                        response['post'] = post.content
                        return JsonResponse(response)

                    new_post = PostModel(author = user, title = post_title, content = post_data.get('content'))
                    if new_post:
                        new_post.save()
                        response['message'] = 'success, post created'
                        return JsonResponse(response, status=200)
                    else:
                        response['error'] = 'No content'
                        return JsonResponse(response, status=400)
                else:
                    return JsonResponse({'message' : f'{username} not logged in, please log in'})
            else:
                return JsonResponse({'message' : f'{username} not exists'})
        else:
            return JsonResponse({'message' : 'Invalid post'})
    
    def get(self, request):
        username = request.GET.get('username')
        if UserModel.objects.filter(username = username).exists() :
            user_ = UserModel.objects.get(username = username) 
            posts = PostModel.objects.filter(author = user_)
            
            response = {
                'username' : user_.username
            }
            posts_ = []            
            for post in posts:
                post_ = {
                    'title' : post.title ,
                    'post' : post.content
                }
                posts_.append(post_)
            
            response['posts'] = posts_
            return JsonResponse(response)
        else:
            return JsonResponse({'message' : 
                                 f"{username} not exists"})
    
@csrf_exempt
def updatePost(request, username):
    if request.method == "PUT":
        try:
            jsonData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'Error in Unmarshalling JSON data'})
        
        if jsonData['content'] is None:
            return JsonResponse({'message' : 'Invalid post'})
        
        if UserModel.objects.filter(username=username).exists() :
            if isAuthenticated(request, username):
                post_title = jsonData.get('title')
                user = UserModel.objects.filter(username=username).first() 
                post = PostModel.objects.filter(author = user, title=post_title).first()

                if post is not None:
                    if post.title != jsonData['title']:
                        return JsonResponse({'message' : 'Title mismatch, Invalid post to update'})
                    
                    if post.content == jsonData.get('content'):
                        return JsonResponse({'message' : 'Not updated, received same post'})
                    else:
                        post.content = jsonData['content']
                        post.save()
                        return JsonResponse({'message' : f'{post.title} post updated'})
                else:
                    return JsonResponse({'message' : 'No post available to update'})
            else:
                return JsonResponse({'message' : f'{username} not logged in, please log in'})
        else:
            return JsonResponse({'message' : f'{username} not exists'})
    else:
        return JsonResponse({'message' : 'Invalid HTTP request'})
