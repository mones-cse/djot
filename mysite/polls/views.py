from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def details(request):
    return HttpResponse("Details")


def result(request):
    return HttpResponse("Result")


def vote(request):
    return HttpResponse("Vote")
