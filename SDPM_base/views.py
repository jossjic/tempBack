from django.http import JsonResponse
from .models import AppUser

def get_users(request):
    users = AppUser.objects.all().values(
        'user_id', 
        'user_email', 
        'user_first_name', 
        'user_last_name', 
        'user_role', 
        'user_picture', 
        'user_norm_accepted', 
        'password'  # Include password
    )
    users_list = list(users)
    return JsonResponse(users_list, safe=False)
