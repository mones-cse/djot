from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Question, Choice


def index(request):
    try:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def details(request, question_id):
    selected_question = get_object_or_404(Question, pk=question_id)
    choices = selected_question.choice_set.all()
    return render(request, 'polls/detail.html', {'choices': choices})


def result(request, question_id):
    return HttpResponse("Result of %s" % question_id)


def vote(request, question_id):
    return HttpResponse("Vote of %s" % question_id)
