from random import shuffle, sample

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.core.cache import cache

from .forms import SignUpForm
from .models import Question, Result, QuizType
from .utils import check_answer

User = get_user_model()

def qiuz(request):
    quizs = QuizType.objects.all()
    context = {
        'quizs': quizs
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def question(request, pk):
    questions = Question.objects.filter(quiz_id=pk)
    if questions.count() > 5:
        questions = sample(list(questions), 5)
    else:
        questions = sample(list(questions), questions.count())
    if request.method == "POST":
        context = check_answer(request)
        cache.delete('questions')
        return render(request, 'quizapp/result.html', context)

    if not cache.get('questions'):
        cache.set('questions', questions, timeout=360)
    questions = cache.get('questions')
    context = {
        'questions': questions,
    }
    return render(request, 'quizapp/question.html', context)


def result_list(request):
    results = Result.objects.all()
    context = {
        'results': results
    }
    return render(request, 'quizapp/result_list.html', context)

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        messages.warning(request, 'qayta urinib kuring')

    form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/register.html', context)

