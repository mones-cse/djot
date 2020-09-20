from django.shortcuts import render
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


def details(request, question_id):
    return HttpResponse("Details of %s" % question_id)


def result(request, question_id):
    return HttpResponse("Result of %s" % question_id)


def vote(request, question_id):
    return HttpResponse("Vote of %s" % question_id)
