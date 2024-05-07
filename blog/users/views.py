from django.http.response import JsonResponse
from django.views.generic import View
import json
from .models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST

@method_decorator(csrf_exempt, name='dispatch')
class UserAccount(View):
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
            existing_user = User.objects.filter(username=username).first()
            if existing_user is None:
                if User.objects.filter(email = email).exists():
                    return JsonResponse({'message' : f'Email is already taken : {email}'})
                
                user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
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
            user = User.objects.filter(username=username).first()
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
        return JsonResponse({'message' : 'Invalid request'})

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            userData = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'Unmarshalling JSON data failed'})
        
        username = userData.get('username')
        password = userData.get('password')

        if User.objects.filter(username=username).exists():
            if isAuthenticated(username, password):
                # login 

                try :
                    if request.session['user_id'] == username:
                        return JsonResponse({'message' : f'{username} already logged in'})
                except KeyError:
                    pass

                request.session['user_id'] = username
                return JsonResponse({'message' : f'{username} logged in'})
            else:
                return JsonResponse({'message' : 'Invalid Credientials'})
        else:
            return JsonResponse({'message' : f'{username} not exists'})
    else:
        return JsonResponse({'message' :'Invalid request'})

def isAuthenticated(username, password):
    user = User.objects.filter(username=username).first()
    return check_password(password, user.password)

@csrf_exempt
@require_POST
def logout_view(request):
    try:
        userData = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
            return JsonResponse({'message' : 'Unmarshalling JSON data failed'})
        
    username = userData.get('username')
    password = userData.get('password')

    if User.objects.filter(username=username).exists():
        if isAuthenticated(username, password):
            # logout
            try :
                if 'user_id' not in request.session:
                    return JsonResponse({'message' : 'Already logged out'})
                
                del request.session['user_id']
            except KeyError:
                pass
            return JsonResponse({'message' : f'{username} logged out'})
        else:
            return JsonResponse({'message' : 'Invalid Credientials'})
    else:
        return JsonResponse({'message' : f'{username} not exists'})