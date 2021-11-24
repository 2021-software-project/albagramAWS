from django.views import View
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    print(request.body)
    return HttpResponse("Post 요청을 잘받았다")