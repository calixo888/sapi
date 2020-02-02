from django.shortcuts import render
from django.contrib import messages
from . import models
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
import random
import string
import json
import requests

# Generates a random API key
def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def index(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if models.APIKey.objects.filter(email=email).exists():
            messages.error(request, "That email is already taken. Please use a different email.")
        else:
            # Generating API key
            apikey = generate_key(20)

            # Saving to database
            models.APIKey.objects.create(email=email, apikey=apikey)

            # Sending API Key to email
            EmailMessage("SAPI API Key", "Thank you for using SAPI!\n\nYour API Key is " + apikey + ". Be sure to save it safely and not forget it.", to=[email]).send()

            # Sending message
            messages.success(request, "Your API key has been sent to " + email + "!")

            return HttpResponseRedirect("/")

    metric_data = requests.get("http://www.sapi.host/api/personal/?apikey=KX05BGUSM5OD9VP3K2J7").json()["0gNM9p6a5P"]
    print(metric_data)
    return render(request, "sapi_app/index.html", context={
        "api_counter": metric_data["api-counter"],
        "total_records": metric_data["total-records"]
    })


def forgot_api_key(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if models.APIKey.objects.filter(email=email).exists():
            # Getting API Key
            apikey = models.APIKey.objects.get(email=email).apikey

            # Sending API Key to email
            EmailMessage("SAPI API Key", "Thank you for using SAPI!\n\nYour API Key is " + apikey + ". Be sure to save it safely and not forget it.", to=[email]).send()

            # Sending message
            messages.success(request, "Your API key has been retrieved! It has been sent to " + email + "!")

            return HttpResponseRedirect("/")

    return render(request, "sapi_app/forgot_api_key.html")


def documentation(request):
    return render(request, "sapi_app/documentation.html")


def get_api_key(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if models.APIKey.objects.filter(email=email).exists():
            messages.error(request, "That email is already taken. Please use a different email.")
        else:
            # Generating API key
            apikey = generate_key(20)

            # Saving to database
            models.APIKey.objects.create(email=email, apikey=apikey)

            # Sending API Key to email
            EmailMessage("SAPI API Key", "Thank you for using SAPI!\n\nYour API Key is " + apikey + ". Be sure to save it safely and not forget it.", to=[email]).send()

            # Sending message
            messages.success(request, "Your API key has been sent to " + email + "!")

            return HttpResponseRedirect("/")

    return render(request, "sapi_app/get_api_key.html")


@csrf_exempt
def personal_storage(request):
    new_data = requests.get("http://www.sapi.host/api/personal/?apikey=KX05BGUSM5OD9VP3K2J7").json()["0gNM9p6a5P"]
    new_data["api-counter"] += 1
    requests.put("http://www.sapi.host/api/personal/?apikey=KX05BGUSM5OD9VP3K2J7&id=0gNM9p6a5P", data=new_data)
    if request.GET.get("apikey"):
        apikey = request.GET.get("apikey")

        # POST REQUEST
        if request.method == "POST":
            new_data["total-records"] += 1
            requests.put("http://www.sapi.host/api/personal/?apikey=KX05BGUSM5OD9VP3K2J7&id=0gNM9p6a5P", data=new_data)
            json_data = list(dict(QueryDict(request.body)).keys())[0]
            json_string = str(json_data)
            models.JSONRecord.objects.create(record_id=generate_key(10), json_string=json_string, user_api_key=apikey)

            return JsonResponse({
                "status": "success",
                "code": 200,
                "message": "Record uploaded successfully."
            })

        # GET REQUEST
        elif request.method == "GET":
            if models.JSONRecord.objects.filter(user_api_key=apikey).exists():
                data = {}
                records = models.JSONRecord.objects.filter(user_api_key=apikey)
                for record in records:
                    json_record = json.loads(record.json_string)
                    data[record.record_id] = json_record
                return JsonResponse(data)
            else:
                return JsonResponse({
                    "status": "failure",
                    "code": 401,
                    "message": "API Key is not valid."
                })

        # DELETE REQUEST
        elif request.method == "DELETE":
            if request.GET.get("id"):
                id = request.GET.get("id")
                if models.JSONRecord.objects.filter(user_api_key=apikey, record_id=id).exists():
                    models.JSONRecord.objects.get(user_api_key=apikey, record_id=id).delete()
                    return JsonResponse({
                        "status": "success",
                        "code": 200,
                        "message": "Record deleted successfully."
                    })
                else:
                    return JsonResponse({
                        "status": "failure",
                        "code": 400,
                        "message": f"No record with ID of {id}. Try checking the ID or your API key again."
                    })
            else:
                return JsonResponse({
                    "status": "failure",
                    "code": 400,
                    "message": "Record ID not provided."
                })

        # PUT REQUEST
        elif request.method == "PUT":
            new_data["total-records"] += 1
            requests.put("http://www.sapi.host/api/personal/?apikey=KX05BGUSM5OD9VP3K2J7&id=0gNM9p6a5P", data=new_data)
            if request.GET.get("id"):
                id = request.GET.get("id")
                if models.JSONRecord.objects.filter(user_api_key=apikey, record_id=id).exists():
                    models.JSONRecord.objects.get(user_api_key=apikey, record_id=id).delete()
                    json_data = list(dict(QueryDict(request.body)).keys())[0]
                    json_string = str(json_data)
                    models.JSONRecord.objects.create(record_id=id, json_string=json_string, user_api_key=apikey)
                    return JsonResponse({
                        "status": "success",
                        "code": 200,
                        "message": "Record updated successfully."
                    })
                else:
                    return JsonResponse({
                        "status": "failure",
                        "code": 400,
                        "message": f"No record with ID of {id}. Try checking the ID or your API key again."
                    })
            else:
                return JsonResponse({
                    "status": "failure",
                    "code": 400,
                    "message": "Record ID not provided."
                })
    else:
        return JsonResponse({
            "status": "failure",
            "code": 400,
            "message": "API Key not provided."
        })
