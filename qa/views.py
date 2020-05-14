from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, AnswerForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from halo.common.decorators import ajax_required



# Create your views here.
def home(request):
    user_count = User.objects.count()
    object_list = Question.objects.all()
    paginator = Paginator(object_list, 5) # 12 questions each page
    page = request.GET.get('page')
    try: 
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        questions = paginator.page(paginator.num_pages)
    return render(request, 'extends/home.html', {'user_count': user_count, 'page': page, 'questions': questions})


def question_detail(request, question):
    user_count = User.objects.count()
    question = get_object_or_404(Question, slug=question)

    # List of active comments for this post
    answers = question.answers.all()

    new_answer = None

    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            # Create Answer object but don't save to database yet
            new_answer = answer_form.save(commit=False)
            # Assign the current question to the answer
            new_answer.question = question
            # Assign user to the answer
            new_answer.user = get_object_or_404(User, username=request.user.username)
            # Save the comment to the database
            new_answer.save()
    else:
        answer_form = AnswerForm()

    return render(request, 'extends/detail.html', {'question': question, 'user_count': user_count, 'answers': answers, 'new_answer': new_answer, 'answer_form': answer_form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but not saving it yet
            new_user = user_form.save(commit=False)
            # Set the choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def logged_in(request):
    return render(request, 'extends/dashboard.html')

@ajax_required
@require_POST
@login_required
def vote(request):
    print(request.POST)
    return JsonResponse({'status':'ok'})
