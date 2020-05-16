from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, AnswerForm, QuestionForm, SearchForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Question, Answer
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from halo.common.decorators import ajax_required
from django.utils.text import slugify


# Create your views here.
def home(request, tag_slug=None):
    search_form = SearchForm()
    user_count = User.objects.count()
    object_list = Question.objects.all()

    # Handle tag filter
    tag = None 
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # Handle search function
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            object_list = Question.objects.filter(title__contains=query)

    paginator = Paginator(object_list, 5) # 5 questions each page
    page = request.GET.get('page')
    try: 
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        questions = paginator.page(paginator.num_pages)

    return render(request, 'extends/home.html', {'user_count': user_count, 'question_count': Question.objects.count() ,'page': page, 'questions': questions, 'tag': tag, 'search_form': search_form})



def question_detail(request, question):
    # Render question detail view
    user_count = User.objects.count()
    question = get_object_or_404(Question, slug=question)
    search_form = SearchForm()
    # List of active answers for this post
    answers = question.answers.all()

    new_answer = None

    # Handle user's answer
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            # Create Answer object but don't save to database yet
            new_answer = answer_form.save(commit=False)
            # Assign the current question to the answer
            new_answer.question = question
            # Assign user to the answer
            new_answer.user = get_object_or_404(User, username=request.user.username)
            # Save the answer to the database
            new_answer.save()
    else:
        answer_form = AnswerForm()

    return render(request, 'extends/detail.html', {'question': question, 'user_count': user_count, 'question_count': Question.objects.count(), 'answers': answers, 'new_answer': new_answer, 'answer_form': answer_form, 'search_form': search_form})


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
def create_question(request):
    user = get_object_or_404(User, username=request.user.username)
    new_question = None
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            new_question = question_form.save(commit=False)
            new_question.slug = slugify(new_question.title)
            new_question.user = user 
            new_question.save()
            for tag in question_form.cleaned_data['tags']:
                new_question.tags.add(tag.lower())
    else:
        question_form = QuestionForm()
    return render(request, 'extends/question.html', {'question_form': question_form, 'user_count': User.objects.count(), 'question_count': Question.objects.count(), 'new_question': new_question})


@ajax_required
@require_POST
@login_required
def voting(request):
    data = request.POST
    if data['action'] == 'upvote':
        if data['qa'] == 'q':
            user = get_object_or_404(User, id=data['id'])
            question = get_object_or_404(Question, slug=data['identity'])
            res = question.upvote(user)
        else: 
            user = get_object_or_404(User, id=data['id'])
            answer = get_object_or_404(Answer, id=data['identity'])
            res = answer.upvote(user)
    else:
        if data['qa'] == 'q':
            user = get_object_or_404(User, id=data['id'])
            question = get_object_or_404(Question, slug=data['identity'])
            res = question.downvote(user)
        else: 
            user = get_object_or_404(User, id=data['id'])
            answer = get_object_or_404(Answer, id=data['identity'])
            res = answer.downvote(user)
   
    return JsonResponse({'status': res})
 

