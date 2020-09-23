# Django Official Tutorial Summary
### Preparation 
  - we need following thing before starting this project 
  - pyenve: we need this to make sure we have multiple python install in our device. Since we have 2.6 already install and the latest Django version requires python 3 version
  - python 3: install python version 3. In this case we will install python 3.8
  - virtualenv: install virtualenv to make sure package are not intirefear with other project
  - Active the project
  - Install django with pip

    ```bash
    $ virtualenv venv -p python3
    $ source venv/bin/active
    $ pip install django
    ```

### Project and app setup
  - check python version
  - Install django project
  - Install django app
  - make migrations
  - migrate
  - runserver

    ```bash
    $ django-admin startproject mysite
    $ python manage.py startapp polls
    $ python manage.py makemigration
    $ python manage.py migrate
    $ python manage.py check
    $ python manage.py runserver
    ```

 - to mamkemigration speciffic app like `polls`

    ```python
    $ python manage.py makemigrations polls
    ```

### Write first sample view
- `HttpResponse` belongs to `django.http`

    ```python
    # polls/views.py
    from django.http import HttpResponse
    
    def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")
    ```

### Update url: part1
- `path` , `include` belongs to `django.urls`
- `path(route, view, kwargs, name)`
    - route is a string that contains a URL pattern.
    - view
    - Arbitrary keyword arguments can be passed
    - Naming your URL lets you refer to it unambiguously from elsewhere in Django

    ```python
    #polls/urls.py
    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
    ]
    ```

    ```python
    # mysite/urls.py
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('polls/', include('polls.urls')),
        path('admin/', admin.site.urls),
    ]
    ```

### Creating models
- models: A model is the single, definitive source of truth about your data.
- `models` belongs to `django.db`
- any class like Question need to inherit `models.Model`
- inside  tah class we can use many filed type . These field type belongs to model classes like `CharField`, `DateTimeField`, `IntegerField`
- we can use `models.ForeignKey` to create foreignkey relation with other model
    - first parameter is another class name here `Question` is the class name in `Choice`
    - `on_delete=models.CASCADE` use to make sure cascade delete

    ```python
    #polls/models.py
    from django.db import models

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)
    ```

    - update settings page to reflect model change in django app

    ```python
    #mysite/settings.py
    INSTALLED_APPS = [
        'polls.apps.PollsConfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    ```

    - to check specific sql for corresponding  migration file like `001`

    ```python
    python manage.py sqlmigrate polls 0001
    ```

### Helpful representation with `__str__()`

```python
#polls/models.py¶
from django.db import models

class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text
```

### Helpful method

```python
#polls/models.py
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    # ...
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```

### Playing with shell
- to active a shell to write code run

```python
$ python manage.py shell
```

- inside shell we can do many thing like this if Model name is `Question, Choice`
    - get data
        - Question.objects.all()
    - store data
        - q = Question(question_text="What's new?", pub_date=timezone.now())
        - q.save()

    ```python
    # Import the model classes we just wrote.
    >>> from polls.models import Choice, Question  

    # No questions are in the system yet.
    >>> Question.objects.all()
    <QuerySet []>

    # Create a new Question.
    # Support for time zones is enabled in the default settings file, so
    # Django expects a datetime with tzinfo for pub_date. Use timezone.now()
    # instead of datetime.datetime.now() and it will do the right thing.
    >>> from django.utils import timezone
    >>> q = Question(question_text="What's new?", pub_date=timezone.now())

    # Save the object into the database. You have to call save() explicitly.
    >>> q.save()

    # Now it has an ID.
    >>> q.id
    1

    # Access model field values via Python attributes.
    >>> q.question_text
    "What's new?"
    >>> q.pub_date
    datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

    # Change values by changing the attributes, then calling save().
    >>> q.question_text = "What's up?"
    >>> q.save()

    # objects.all() displays all the questions in the database.
    >>> Question.objects.all()
    <QuerySet [<Question: Question object (1)>]>
    ```

- fillter query: `Question.objects.filter(id=1)`
- Display any choices from the **related** object set.
    - q = Question.objects.get(pk=1)
    - q.choice_set.all()
- Create choice: `q.choice_set.create(choice_text='Not much', votes=0)`
- delete one of the choices.
    - c = q.choice_set.filter(choice_text__startswith='Just hacking')
    - c.delete()

    ```python
    >>> from polls.models import Choice, Question

    # Make sure our __str__() addition worked.
    >>> Question.objects.all()
    <QuerySet [<Question: What's up?>]>

    # Django provides a rich database lookup API that's entirely driven by
    # keyword arguments.
    >>> Question.objects.filter(id=1)
    <QuerySet [<Question: What's up?>]>
    >>> Question.objects.filter(question_text__startswith='What')
    <QuerySet [<Question: What's up?>]>

    # Get the question that was published this year.
    >>> from django.utils import timezone
    >>> current_year = timezone.now().year
    >>> Question.objects.get(pub_date__year=current_year)
    <Question: What's up?>

    # Request an ID that doesn't exist, this will raise an exception.
    >>> Question.objects.get(id=2)
    Traceback (most recent call last):
        ...
    DoesNotExist: Question matching query does not exist.

    # Lookup by a primary key is the most common case, so Django provides a
    # shortcut for primary-key exact lookups.
    # The following is identical to Question.objects.get(id=1).
    >>> Question.objects.get(pk=1)
    <Question: What's up?>

    # Make sure our custom method worked.
    >>> q = Question.objects.get(pk=1)
    >>> q.was_published_recently()
    True

    # Give the Question a couple of Choices. The create call constructs a new
    # Choice object, does the INSERT statement, adds the choice to the set
    # of available choices and returns the new Choice object. Django creates
    # a set to hold the "other side" of a ForeignKey relation
    # (e.g. a question's choice) which can be accessed via the API.
    >>> q = Question.objects.get(pk=1)

    # Display any choices from the related object set -- none so far.
    >>> q.choice_set.all()
    <QuerySet []>

    # Create three choices.
    >>> q.choice_set.create(choice_text='Not much', votes=0)
    <Choice: Not much>
    >>> q.choice_set.create(choice_text='The sky', votes=0)
    <Choice: The sky>
    >>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

    # Choice objects have API access to their related Question objects.
    >>> c.question
    <Question: What's up?>

    # And vice versa: Question objects get access to Choice objects.
    >>> q.choice_set.all()
    <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
    >>> q.choice_set.count()
    3

    # The API automatically follows relationships as far as you need.
    # Use double underscores to separate relationships.
    # This works as many levels deep as you want; there's no limit.
    # Find all Choices for any question whose pub_date is in this year
    # (reusing the 'current_year' variable we created above).
    >>> Choice.objects.filter(question__pub_date__year=current_year)
    <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

    # Let's delete one of the choices. Use delete() for that.
    >>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
    >>> c.delete()
    ```

### Django Admin and admin panel customization
- create superuser

    ```python
    $ python manage.py createsuperuser
    ```

- add app like poll into admin panel

    ```python
    # polls/admin.py¶
    from django.contrib import admin

    from .models import Question

    admin.site.register(Question)
    ```

### Update url: part2

```python
#polls/urls.py¶
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

### View
- create simple view

```python
#polls/views.py¶
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

- simple index view

```python
#polls/views.py¶
from django.http import HttpResponse

from .models import Question

def index(request):
latest_question_list = Question.objects.order_by('-pub_date')[:5]
output = ', '.join([q.question_text for q in latest_question_list])
return HttpResponse(output)

# Leave the rest of the views (detail, results, vote) unchanged

```

- index view with template
    - user loader to load the template
    - user template.render to render the template with context

```python
from django.http import HttpResponse
from django.template import loader

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

- template
    - template must create with a specific folder structure
    - Django will choose the first template it finds whose name matches, and if you had a template with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the best way to ensure this is by namespacing them.
    - so insted of putting `index.html` file in `polls/templates` put it into `polls/polls/templates`

    ```python
    #polls/templates/polls/index.html¶
    {% if latest_question_list %}
        <ul>
        {% for question in latest_question_list %}
            <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}
    ```

- detail.html
    - `question.choice_set.all` is interpreted as the Python code `question.choice_set.all()`, which returns an iterable of Choice objects

    ```python
    #polls/templates/polls/detail.html¶
    <h1>{{ question.question_text }}</h1>
    <ul>
    {% for choice in question.choice_set.all %}
        <li>{{ choice.choice_text }}</li>
    {% endfor %}
    </ul>
    ```

- result.html

```python
#polls/templates/polls/results.html¶
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

### Update url: remove hardcoding
- update app name
- update name attribute in view

    ```python
    #polls/urls.py¶
    from django.urls import path

    from . import views

    app_name = 'polls'
    urlpatterns = [
        path('', views.index, name='index'),
        path('<int:question_id>/', views.detail, name='detail'),
        path('<int:question_id>/results/', views.results, name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]
    ```

- remove hard coding

    ```python
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
    ```

### Minimal form
- form
    - action: url
    - method: POST/GET
- csrf_token: to prevent Cross Site Request Forgeries  all POST forms that are targeted at internal URLs should use the {% csrf_token %} template tag.
- input
    - type: text/radio/submit
    - value: values
    - id: require for label
    - name: name
- label
    - for : same as input id
    - value : text
- selected input POST name as key and value as value

    ```html
    #polls/templates/polls/detail.html
    <h1>{{ question.question_text }}</h1>

    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

    <form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
    <input type="submit" value="Vote">
    </form>
    ```

- update view
    - update vote using `selected_choice.votes += 1`
    - but this does not update db we need to use `selected_choice.save()`

    ```python
    #polls/views.pp
    from django.shortcuts import get_object_or_404, render
    from django.urls import reverse

    from .models import Choice, Question
    # ...
    def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    ```

### Shortcuts
- render

```python
#polls/views.py¶
from django.shortcuts import render

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

- Raising a 404 error

```python
# polls/views.py¶
from django.http import Http404
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```

- get_object_or_404()

```python
from django.shortcuts import get_object_or_404, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```
