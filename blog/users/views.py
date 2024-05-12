from django.http.response import JsonResponse
from django.views.generic import View
import json
from .models import UserModel
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST

@method_decorator(csrf_exempt, name='dispatch')
class UserAccountHandler(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'Error in unmarshalling data'})
        
        first_name = data.get('first name')
        last_name = data.get('last name')
        username = data.get('username')
        email = data.get('Email')
        password = data.get('password')

        existing_user = UserModel.objects.filter(username=username).first()
        if existing_user is not None:
            return JsonResponse({'message' : f'User exists : {username}'})
        
        if UserModel.objects.filter(email = email).exists():
            return JsonResponse({'message' : f'Email is already taken : {email}'})
        
        if first_name and last_name and username and email and password:
            user = UserModel(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.save()
            return JsonResponse({'message' : f'Account created : {username}'})
           
        return JsonResponse({'message', 'Invalid details'})


@csrf_exempt
def updatePassword(request, username):
    if request.method == "PUT":
        if username is None:
            return JsonResponse({'message' : 'Invalid User'})
        try:
            passwordData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'Unmarshalling JSON data failed'})

        newPassword = passwordData.get('New Password')
        user = UserModel.objects.filter(username=username).first()
        if newPassword is None or user is None:
            return JsonResponse({'message' : 'Invalid details'}) 
        
        if check_password(newPassword, user.password):
            return JsonResponse({'message' : 'New Password and Old password are same'})
        
        user.password = newPassword
        user.save()

        # log out after update
        try :
            del request.session['user_id']
        except KeyError:
            pass
        return JsonResponse({'message' : 'Password Updated'})
    
    return JsonResponse({'message' : 'Invalid HTTP request'})

@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({'message' :'Invalid HTTP request'})
    
    try:
        userData = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'message' : 'Unmarshalling JSON data failed'})
    
    username = userData.get('username')
    password = userData.get('password')
    user = UserModel.objects.filter(username=username).first()
    
    if user is None:
        return JsonResponse({'message' : f'{username} not exists'})
    
    if isAuthenticated(request, username):
        return JsonResponse({'message' : f'{username} already logged in'})
    
    if check_password(password, user.password):
        request.session['user_id'] = username
        return JsonResponse({'message' : f'{username} logged in'})

    return JsonResponse({'message' : f'{username} not exists or Invalid credientials'})

def isAuthenticated(request, username):
    try :
        return 'user_id' in request.session and request.session['user_id'] == username
    except KeyError:
        pass 

@csrf_exempt
@require_POST
def logout_view(request):
    if request.method == "POST":
        try:
            userData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
                return JsonResponse({'message' : 'Unmarshalling JSON data failed'})
            
        username = userData.get('username')
        password = userData.get('password')

        user = UserModel.objects.filter(username=username).first()
        if user is None:
            return JsonResponse({'message' : f'{username} not exists'})
        
        if not isAuthenticated(request, username):
            return JsonResponse({'message' : f'{username} not logged in or already logged out'})
        
        if not check_password(password, user.password):
            return JsonResponse({'message' : 'Invalid Credientials'})

        try:
            del request.session['user_id']
        except KeyError:
            pass
        return JsonResponse({'message' : f'{username} logged out'})

    return JsonResponse({'message' :'Invalid HTTP request'})