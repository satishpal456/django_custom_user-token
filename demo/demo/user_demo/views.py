from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User
from django.core.mail import EmailMessage
from random import randint
from datetime import datetime, timedelta
from rest_framework import generics,mixins
# Create your views here.
def home(request):
	return HttpResponse("satish pal")

@csrf_exempt
@api_view(["POST"])
def create_user_regi(request):
	try:
		email = request.data["email"]
		password = request.data["password"]
		email_avai = User.objects.filter(email=email).exists()
		if email_avai:
			return Response({"error":"email already exists"},status=HTTP_400_BAD_REQUEST)
		else:
			user = User.objects.create_user(email=email,password=password)
			return Response({"success":"user Created successfully"},status=HTTP_200_OK)
	except Exception as e:
		print("error==>",e)
		return Response({"error":"something wrong"},status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@permission_classes((AllowAny))
@api_view(["POST"])
def login_user(request):
	try:
		email = request.data["email"]
		password = request.data["password"]
		user = authenticate(email=email,password=password)
		if user:
			token = Token.objects.get_or_create(user=user)
			print("data===>",token[0])
			json_data = {"email":email,"token":str(token[0])}
			res_data = {"status_code": 200, "status": "success", "message": ("user Details"), "data": json_data}
			return Response(status=HTTP_200_OK,data=res_data)
		else:
			return Response({"error":"Not a valid user"},status=HTTP_400_BAD_REQUEST)
	except Exception as e:
		print("error login ==>",e)
		return Response({"error":"something wrong"},status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@permission_classes((AllowAny))
@api_view(["GET"])
def access_data(request):
	return Response({"SUCCESS":"ACCESS"},status=HTTP_200_OK)