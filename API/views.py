import os

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.conf import settings
from SDPM_base.models import Item
from .serializers import  ItemSerializer
import pysd

@api_view(['GET'])
def getData(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def getBunnies(request):
    model_file_path = os.path.join(settings.BASE_DIR, 'API', 'assets', 'test.mdl')
    model = pysd.read_vensim(model_file_path)
    #print(model.components)
    birth_rate = request.data.get('Birth Rate')
    # Check if the 'Birth Rate' parameter is provided and valid
    if birth_rate is None:
        return Response({'error': 'Birth Rate parameter is required'}, status=400)
    try:
        birth_rate = float(birth_rate)
    except ValueError:
        return Response({'error': 'Birth Rate must be a valid number'}, status=400)
    result = model.run({'Birth Rate': birth_rate})

    print(result.index)
    print(result['Population'])
    return Response(result)