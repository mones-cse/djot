from django.shortcuts import render
from django.http import HttpResponse

from .models import Question


def index(request):
    q = Question.objects.all()
    question_list = []
    for each in q:
        question_list.append(each.question_text)
    question_list_text = ', '.join(question_list)
    return HttpResponse(question_list_text)


def details(request, question_id):
    return HttpResponse("Details of %s" % question_id)


def result(request, question_id):
    return HttpResponse("Result of %s" % question_id)


def vote(request, question_id):
    return HttpResponse("Vote of %s" % question_id)
