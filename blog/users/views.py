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

        if first_name and last_name and username and email and password:
            existing_user = UserModel.objects.filter(username=username).first()
            if existing_user is None:
                if UserModel.objects.filter(email = email).exists():
                    return JsonResponse({'message' : f'Email is already taken : {email}'})
                
                user = UserModel(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                return JsonResponse({'message' : f'Account created : {username}'})
            else:
                return JsonResponse({'message' : f'User exists : {username}'})
        else:
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
        if username and newPassword:
            user = UserModel.objects.filter(username=username).first()
            if user is not None:
                if not check_password(newPassword, user.password):
                    user.password = newPassword
                    user.save()

                    # log out after update
                    try :
                        del request.session['user_id']
                    except KeyError:
                        pass

                    return JsonResponse({'message' : 'Password Updated'})
                else:
                    return JsonResponse({'message' : 'New Password and Old password are same'})
            else:
                return JsonResponse({'message' : f'Unknown user : {username}'})  
        else:
            return JsonResponse({'message' : 'Invalid credientials'})  
    else:
        return JsonResponse({'message' : 'Invalid HTTP request'})

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            userData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'Unmarshalling JSON data failed'})
        
        username = userData.get('username')
        password = userData.get('password')

        user = UserModel.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            if isAuthenticated(request, username):
                return JsonResponse({'message' : f'{username} already logged in'})
            else:
                request.session['user_id'] = username
                return JsonResponse({'message' : f'{username} logged in'})
        else:
            return JsonResponse({'message' : f'{username} not exists or Invalid credientials'})
    else:
        return JsonResponse({'message' :'Invalid HTTP request'})

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
        if user and check_password(password, user.password):
            if not isAuthenticated(request, username):
                return JsonResponse({'message' : f'{username} not logged in or already logged out'})
            else:
                try:
                    del request.session['user_id']
                except KeyError:
                    pass
                return JsonResponse({'message' : f'{username} logged out'})
        else:
            return JsonResponse({'message' : 'Invalid Credientials'})
    else:
        return JsonResponse({'message' :'Invalid HTTP request'})