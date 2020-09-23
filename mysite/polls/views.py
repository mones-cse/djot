from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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
    return render(request, 'polls/detail.html', {'selected_question': selected_question})


def result(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except:
        return render(request,
                      'polls/detail.html',
                      {'selected_question': question,
                       'error_message': 'Dude you need to choose something!!!'}
                      )
    else:
        selected_choice.votes = selected_choice.votes + 1
        selected_choice.save()
        print(reverse('polls:result', args=(question_id,)))
        return HttpResponseRedirect( reverse('polls:result', args=(question_id,)))


# def votes(request, question_id):
#     try:
#         selected_choice = get_object_or_404(Question, pk=question_id).choice_set.get(pk=request.POST['choice'])
#     except:
#         raise Http404("Question does not exist")
#     else:
#
#         return render(request,'polls/vote.html',{'selected_choice':selected_choice})
