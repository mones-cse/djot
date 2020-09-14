import datetime
from django.db import models
from django.utils import timezone


# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

# shll command
# from polls.models import Question
# from django.utils import timezone
# q = Question(question_text="First Question", pub_date=timezone.now())
# q.save()
# q1 = Question.objects.get(pk=1)
# q1.choice_set.create(choice_text="choice 1",votes=0)