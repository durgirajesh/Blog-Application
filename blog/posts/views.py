import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CommentModel, PostModel, ReplyModel
from django.views import View
from django.utils.decorators import method_decorator
from users.models import UserModel
from users.views import isAuthenticated

@method_decorator(csrf_exempt, name='dispatch')
class PostCreateHandler(View):
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

@method_decorator(csrf_exempt, name='dispatch')
class PostUpdateHandler(View):
    def put(self, request, username):
        try:
            jsonData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'Error in Unmarshalling JSON data'})
        
        if 'content' not in jsonData:
            return JsonResponse({'message' : 'Invalid Request, need content to update'})
        
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
                             'author' : post.author.username,
                             'title' : post.title})
    
    def delete(self, request, username):       
        if not isAuthenticated(request, username):
            return JsonResponse({'message' : f'{username} not logged in, please log in'})
        
        title = request.GET.get('title')
        author = UserModel.objects.get(username=username)
        if  title is None:
            posts = PostModel.objects.filter(author = author)
            for post in posts:
                post.delete()    
            return JsonResponse({'message' : f'All posts deleted from {username}'})
        
        # delete only particular post
        post = PostModel.objects.filter(author = author, title = title).first()
        if post is None:
            return JsonResponse({'message' : 'Post not exists'})
        post.delete()
        return JsonResponse({'message' : f'post of {title} from {username} is deleted'})

@method_decorator(csrf_exempt, name='dispatch')
class CommentsHandler(View):
    def post(self, request):
        try:
            commentData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : "Couldn't unmarshall Data"})
        
        if commentData is None or len(commentData) < 3:
            return JsonResponse({'message' : 'Invalid Json Data'})
        
        postUser = commentData.get('author')
        postTitle = commentData.get('title')
        commenter = commentData.get('username')
        comment = commentData.get('comment')

        author = UserModel.objects.get(username = postUser)
        commenterObj_ = UserModel.objects.get(username = commenter) 
        if author is None or commenterObj_ is None:
            return JsonResponse({'message' : 'User doesnt exist'})
        
        postObj = PostModel.objects.filter(author = author, title = postTitle).first()   
        if postObj is None :
            return JsonResponse({'message' : 'Invalid User Details'})
        
        if 'replied' in commentData:
            replyObj = commentData.get('replied')

            if replyObj is None:
                return JsonResponse({'message' : 'No reply given'})
            
            username = replyObj.get('username')
            if not UserModel.objects.filter(username=username).exists():
                return JsonResponse({'message' : f'{username}, replied user not exists'})
            
            reply = replyObj.get('reply')
            user = UserModel.objects.filter(username=username).first()

            if user is None:
                user = UserModel(username = username)

            replyData = ReplyModel(reply=reply, username=user)
            commenterObj = CommentModel.objects.filter(post = postObj, comment = comment, commenter = commenterObj_).first()
            if commenterObj is None:
                return JsonResponse({'message' : 'No comment to reply'})

            if commenterObj.RID is not None:
                return JsonResponse({'message' : 'Already replied'})
            
            replyData.save()
            commenterObj.RID = replyData
            commenterObj.save()
            return JsonResponse({'message' : 'replied successfull'})
            
        commentObj = CommentModel(post=postObj, comment = comment, commenter = commenterObj_)
        commentObj.save()
        return JsonResponse({'message' : f'Comment added from {commenter}'})

    
    def get(self, request):
        username = request.GET.get('author')
        title = request.GET.get('title')

        author = UserModel.objects.filter(username=username).first()
        response = {}
        if author is None:
            return JsonResponse({'message' : 'No user exists'})
        
        response['author'] = username
        if title :
            post = PostModel.objects.filter(author=author, title=title).first()
            if post is None:
                return JsonResponse({'message' : f'No post created for {author.username}'})
            
            response['post'] = post.title
            comments = []
            postComments = CommentModel.objects.filter(post=post)
            for postComment in postComments:
                Comment = {
                    'username' : postComment.commenter.username, # type: ignore
                    'comment' : postComment.comment
                }
                if postComment.RID :
                    Comment['username(reply)'] = postComment.RID.username.username
                    Comment['reply'] = postComment.RID.reply
                comments.append(Comment)
            response["Comments"] = comments # type: ignore
            return JsonResponse(response)

        posts = PostModel.objects.filter(author=author)
        userPosts = []
        for post in posts:
            UserPosts = {
                'title' : post.title,
                'post' : post.content
            }
            comments = []
            postComments = CommentModel.objects.filter(post=post)
            for postComment in postComments:
                Comment = {
                    'username' : postComment.commenter.username, # type: ignore
                    'comment' : postComment.comment
                }

                if postComment.RID is None:
                    comments.append(Comment)
                    continue

                Comment['username(reply)'] = postComment.RID.username.username
                Comment['reply'] = postComment.RID.reply
                comments.append(Comment)

            UserPosts["Comments"] = comments # type: ignore
            userPosts.append(UserPosts)
        response["posts"] = userPosts # type: ignore
        return JsonResponse(response)
                