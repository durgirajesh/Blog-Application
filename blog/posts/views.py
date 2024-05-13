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

        # validate post_data
        if post_data is None or len(post_data) != 3 or post_data['username'] is None or post_data['title'] is None or post_data['content'] is None:
            return JsonResponse({'message' : 'Invalid post'})

        # validate user
        username = post_data.get('username')
        user = UserModel.objects.filter(username=username).first()
        if user is None:
            return JsonResponse({'message' : f'{username} not exists'})
        
        # valid user authentication
        if not isAuthenticated(request, username):
            return JsonResponse({'message' : f'{username} not logged in, please log in'})
        
        post_title = post_data.get('title')
        post = PostModel.objects.filter(author = user, title=post_title).first()

        if post is not None:
            response['message'] = 'Post already exists'
            response['title'] = post.title
            response['post'] = post.content
            return JsonResponse(response)

        new_post = PostModel(author = user, title = post_title, content = post_data.get('content'))
        new_post.save()
        response['message'] = 'success, post created'
        return JsonResponse(response, status=200)
    
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

                post_['created at'] = post.createdAtTime # type: ignore
                post_['updated at'] = post.updatedAtTime # type: ignore
                posts_.append(post_)
            
            response['posts'] = posts_ # type: ignore
            return JsonResponse(response)
        
        return JsonResponse({'message' : f"{username} not exists"})
    
@csrf_exempt
def updatePost(request, username):
    if request.method == "PUT":
        try:
            jsonData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'Error in Unmarshalling JSON data'})
        
        if jsonData['content'] is None:
            return JsonResponse({'message' : 'Invalid post'})
        
        if not UserModel.objects.filter(username=username).exists() :
            return JsonResponse({'message' : f'{username} not exists'})
        
        if not isAuthenticated(request, username):
            return JsonResponse({'message' : f'{username} not logged in, please log in'})
        
        post_title = jsonData.get('title')
        user = UserModel.objects.filter(username=username).first() 
        post = PostModel.objects.filter(author = user, title=post_title).first()

        if post is None:
            return JsonResponse({'message' : 'No post available to update'})
        
        if post.title != jsonData['title']:
            return JsonResponse({'message' : 'Title mismatch, Invalid post to update'})
            
        if post.content == jsonData.get('content'):
            return JsonResponse({'message' : 'Not updated, received same post'})
    
        # After all checks, update the post
        post.content = jsonData['content']
        post.save()
        return JsonResponse({'message' : 'post updated', 
                             'title' : post.title})
    
    return JsonResponse({'message' : 'Invalid HTTP request'})
