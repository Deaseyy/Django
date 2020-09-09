from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Photos
from home.circle.models import News


@api_view(['GET'])
def get_num(request):
    photo_num = Photos.objects.count()
    dynamic_num = News.objects.count()
    return Response({'code': 200, 'photo_num': photo_num, 'dynamic_num':dynamic_num})
