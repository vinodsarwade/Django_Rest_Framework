from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from firstapp.models import Employee

def employeeview(request):
    emp = {"id":123, "name":"john", "salary":6789}
    return JsonResponse(emp)

def employeeview(request):
    data = Employee.objects.all()
    responce = {"employee":list(data.values('name','salary'))}
    return JsonResponse(responce)