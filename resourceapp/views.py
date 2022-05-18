from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import User,Resources, BookedResources
from .serializers import UserSerializer, UserData, ResourcesSerializer, BookedResourcesSerializer
from .udf import generate_token, authenticate_token


@csrf_exempt
def user_signup(request):
    try:
        if request.method == "POST":
            data = JSONParser().parse(request)
            serialized_data = UserSerializer(data=data)
            if serialized_data.is_valid():
                saved_data = serialized_data.save()
                token = generate_token({"user": saved_data})
                return JsonResponse({"success": True, "error_code": 200, "message": {},"data": {"user_data": UserData(saved_data).data, "token": token}})
            return JsonResponse({"success": False, "error_code": 101, "message": serialized_data.errors, "data": {}})

        elif request.method == "GET":
            data = JSONParser().parse(request)
            token = data.get('token')
            user_id = data.get('user_id')
            token_auth = authenticate_token({"token": token, "user_id": user_id})
            if token_auth[0]:
                return JsonResponse({"success": True, "error_code": 200, "message": {}, "data": {"user_data": token_auth[1]}})
            return JsonResponse({"success": False, "error_code": 101, "message": {"authentication": "Invalid Token"}, "data": {}})
        return JsonResponse({"success": False, "error_code": 102, "message":{"method": f"Invalid method {request.method}"}, "data": {}})
    except Exception as e:
        return JsonResponse({"success": False, "error_code": 103, "message": {"unknown": f"{e}"}, "data": {}})

@csrf_exempt
def user_login(request):
    try:
        if request.method == "POST":
            data = JSONParser().parse(request)
            mobile_no = data.get('mobile_no')
            password = data.get('password')
            try:
                user_data = User.objects.get(mobile_no=mobile_no)
            except Exception as e:
                return {"success":False, "error_code": 103, "message":{"mobile_no": f"Invalid mobile no  {mobile_no}"}}
            if check_password(password, user_data.password):
                token = generate_token({"user": user_data})
                return JsonResponse({"success": True, "error_code": 200, "message": {},"data": {"user_data": UserData(user_data).data, "token": token}})
            return JsonResponse({"success": False, "error_code": 101, "message": {"authentication":"Given Password is not correct"}, "data": {}})
        return JsonResponse({"success": False, "error_code": 102, "message":{"method": f"Invalid method {request.method}"}, "data": {}})
    except Exception as e:
        return JsonResponse({"success": False, "error_code": 103, "message": {"unknown": f"{e}"}, "data": {}})


def resource_view(request):
    try:
        if request.method == "GET":
            data = JSONParser().parse(request)
            token = data.get('token')
            user_id = data.get('user_id')
            token_auth = authenticate_token({"token": token, "user_id": user_id})
            if token_auth[0]:
                resources = Resources.objects.all().exclude(quantity_available=0)
                resources = ResourcesSerializer(resources,many=True).data
                return JsonResponse({"success": True, "error_code": 200, "message": "", "data":{"resources": resources}})
            return JsonResponse({"success": False, "error_code": 101, "message": {"authentication": "Invalid Token"}, "data": {}})
        return JsonResponse({"success": False, "error_code": 102, "message": {"method": f"Invalid method {request.method}"}, "data": {}})
    except Exception as e:
        return JsonResponse({"success": False, "error_code": 103, "message": {"unknown": f"{e}"}, "data": {}})


@csrf_exempt
def booked_resource(request):
    try:
        if request.method == "GET":
            data = JSONParser().parse(request)
            token = data.get('token')
            user_id = data.get('user_id')
            token_auth = authenticate_token({"token": token, "user_id": user_id})
            if token_auth[0]:
                booked_data = BookedResources.objects.filter(user_id=user_id)
                serialized_data = BookedResourcesSerializer(booked_data, many=True).data
                return JsonResponse({"status": True, "error_code": 200, "message": {}, "data": {"booked":serialized_data}})
            return JsonResponse({"success": False, "error_code": 101, "message": {"authentication": "Invalid Token"}, "data": {}})

        elif request.method == "POST":
            data = JSONParser().parse(request)
            token = data.get('token')
            user_id = data.get('user_id')
            token_auth = authenticate_token({"token": token, "user_id": user_id})
            if token_auth[0]:
                serialized_data = BookedResourcesSerializer(data=data)
                if serialized_data.is_valid():
                    serialized_data.save(user_id=user_id)
                    resources = serialized_data.validated_data.get('resources')
                    resources.quantity_available = resources.quantity_available - serialized_data.validated_data.get('quantity')
                    resources.quantity_sold = resources.quantity_sold + serialized_data.validated_data.get('quantity')
                    resources.save()
                    booked_data = BookedResources.objects.filter(user_id=user_id)
                    serialized_data = BookedResourcesSerializer(booked_data, many=True).data
                    return JsonResponse({"status": True, "error_code": 200, "message": {}, "data": {"booked": serialized_data}})
                return JsonResponse({"status": False, "error_code": 101, "message": serialized_data.errors, "data": {}})
            return JsonResponse({"success": False, "error_code": 101, "message": {"authentication": "Invalid Token"}, "data": {}})
        return JsonResponse({"success": False, "error_code": 102, "message": {"method": f"Invalid method {request.method}"},"data": {}})
    except Exception as e:
        return JsonResponse({"success": False, "error_code": 101, "message": {"authentication": "Invalid Token"}, "data": {}})










