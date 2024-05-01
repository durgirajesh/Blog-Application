import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import post_model 
from .forms import post_form

@csrf_exempt
def create_post(request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode('utf-8'))
        post_title = post_data.get('title')

        response = {}
        posts = post_model.objects.filter(title=post_title).first()
        if posts :
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
    else:
        return JsonResponse({'error' : 'Invalid HTTP request'}, status=400)

def get_post(request):
    pass
