from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# from django.template import loader
# from django.http import Http404

from .models import Question, Choice

# index with http_response
"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('myapp/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
"""

# index shortcut with render
"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'myapp/index.html', context)

"""

# index with Amendviews


class IndexView(generic.ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last fivce published questions (not including
        those set to be published in the future)
        """
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

# detail_view with render


"""
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'myapp/detail.html', {'question': question})
"""

# shortcut with render and get_object_or_404

""""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/detail.html', {'question': question})
"""


class DetailView(generic.DetailView):
    model = Question
    template_name = 'myapp/detail.html'

    def get_queryset(self):
        """
        Excludes any question that aren't published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# resultsview with shortcust
"""
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/results.html', {'question': question})
"""

# results with Amend views


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'myapp/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myapp:results',
                                            args=(question.id,)))
