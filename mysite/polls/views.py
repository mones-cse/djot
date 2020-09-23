from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render

from .models import Question


def index(request):
    try:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request,'polls/index.html',context)


def details(request, question_id):
    return HttpResponse("Details of %s" % question_id)


def result(request, question_id):
    return HttpResponse("Result of %s" % question_id)


def vote(request, question_id):
    return HttpResponse("Vote of %s" % question_id)
