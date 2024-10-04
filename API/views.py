import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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


@swagger_auto_schema(
    method='post',
    operation_description="Endpoint que ejecuta un modelo y devuelve una matriz de resultados según el parámetro 'Birth Rate'.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'Birth Rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='Tasa de nacimiento', example=1.5)
        },
        required=['Birth Rate']
    ),
    responses={
        200: openapi.Response('OK', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Population': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_NUMBER), description='Datos de población'),
                'index': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Fechas de la simulación')
            }
        )),
        400: 'Bad Request: Birth Rate parameter is missing or invalid'
    }
)
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


@api_view(['POST'])
def helloWorld(request):
    return Response({"message": "Hello World!"})