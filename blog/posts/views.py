import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import post_model 
from .forms import post_form
from django.views.generic import View
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class Posts(View):
    def post(self, request):
        response = {}
        post_data = json.loads(request.body.decode('utf-8'))
        
        post_title = post_data.get('title')
        posts = post_model.objects.filter(title=post_title).first()

        if posts is not None:
            response['message'] = 'Title Already Exists'
            response[posts.title] = posts.content

            return JsonResponse(response)
        
        post_data_form = post_form(post_data)
        if post_data_form.is_valid():
            post_data_form.save()
            response['message'] = 'success'
            return JsonResponse(response, status=200)
        else:
            response['error'] = post_data_form.errors
            return JsonResponse(response, status=400)
    
    def put(self, request):
        try:
            jsonData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'Error in Unmarshalling JSON data'})
        
        title_ = request.GET.get('title')
        posts = post_model.objects.filter(title = title_).first()
        if posts is None:
            return JsonResponse({'message' : 'No Post to update'})
        
        description = jsonData.get('content')
        if description is not None:
            if description == posts.content :
                return JsonResponse({'message' : 'Same content, no update needed'})
            
            posts.content = description
            posts.save()
            return JsonResponse({'message' : 'succcess'}, status=200)
        else:
            return JsonResponse({'message' : 'Error, Invalid Description'})
        
