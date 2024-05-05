from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
def viewsreturn(request):
    return HttpResponse("hhhh hello world from django.shortcuts")
class retinfo(APIView):
    def post(self, request, *args, **kwargs):
        return Response({"retinfo": "I got you"})

