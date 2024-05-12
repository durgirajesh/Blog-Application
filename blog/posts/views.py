import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PostModel, CommentsModel
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

                post_['created at'] = post.createdAtTime
                post_['updated at'] = post.updatedAtTime
                posts_.append(post_)
            
            response['posts'] = posts_
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
        return JsonResponse({'message' : f'{post.title} post updated'})
    
    return JsonResponse({'message' : 'Invalid HTTP request'})

@method_decorator(csrf_exempt, name='dispatch')
class CommentsHandler(View):
    def post(self, request):
        try:
            jsonData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : "Couldn't Unmarshall JSON Data"})
        
        username = jsonData['username']
        postTitle = jsonData['title']
        comment = jsonData['comment']

        if not UserModel.objects.filter(username=username).exists():
            return JsonResponse({'message' : f'{username} not exists'})
        
        post = PostModel.objects.filter(author = username, title = postTitle).first()
        if post is None:
            return JsonResponse({'message' : 'Error, Post not available'})
        
        new_comment = CommentsModel(post = post, comment = comment)
        new_comment.save()
        return JsonResponse({'message' : f'comment added for : {postTitle}'})  

    def get(self, request):
        username = request.GET.get('username')
        if not UserModel.objects.filter(username = username).exists():
            return JsonResponse({'message' : f'{username} not exists'})
        
        __user = UserModel.objects.get(username = username)
        __posts = PostModel.objects.filter(author = __user)

        if __posts.count() < 0:
            return JsonResponse({'message' : f'No posts available for {username}'})
        
        __response = {'username' : username}
        __titles = []

        for __post in __posts:
            __post_ = PostModel.objects.get(author = __user, title = __post.title)
            __commentResponse = {'title' : __post.title}
            __comments = []

            if __post_ is not None:
                __commentslist = CommentsModel.objects.filter(post = __post_)
                for __comment in __commentslist:
                    __comments.append(__comment.comment)
                
                __commentResponse['comments'] = __comments
            
            __titles.append(__commentResponse)
        
        __response['posts'] = __titles
        return JsonResponse(__response, status=200)
                
    def put(self, request):
        pass