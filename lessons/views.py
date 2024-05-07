from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.views import APIView
# from rest_framework.response import Response
# Create your views here.
# class retinfo(APIView):
#     def post(self, request, *args, **kwargs):
#         return Response({"retinfo": "I got you"})

def viewsreturn(request, *args, **kwargs):
    return HttpResponse({"retinfoismine",2335201314})
@csrf_exempt
def retinfo(request):
    print(request)
    data = [
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 30},
        {'name': 'Charlie', 'age': 35}
    ]
    return JsonResponse(data, safe=False)

