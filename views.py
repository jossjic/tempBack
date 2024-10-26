from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import AppUser

@api_view(['GET'])
@permission_classes([AllowAny])
def get_users(request):
    users = AppUser.objects.all().values('user_id', 'user_email', 'user_first_name', 'user_last_name')
    users_list = list(users)
    return JsonResponse(users_list, safe=False)

