from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.sessions.models import Session
from django.db import IntegrityError
import datetime
import json

from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"Not unique name"})
        else:
            #missmatch passwords
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"Didn't match passwords"})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password didn\'t match'})
        else:
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.executor = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Wrong data passed in! Try again ;)'})


def currenttodos(request):
    todos = Todo.objects.filter(executor=request.user, close_date__isnull=True).order_by('-priority')
    return render(request, 'todo/currenttodos.html', {'todos': todos})


def closedtodos(request):
    todos = Todo.objects.filter(executor=request.user, close_date__isnull=False).order_by('-close_date')
    return render(request, 'todo/currenttodos.html', {'todos': todos})


def detailtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, executor=request.user)
    status = ''
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if request.POST['status'] in ['COMPLITED', 'FAILED']:
            form.instance.close_date = datetime.datetime.now()
        if form.is_valid():
            form.save()
            status = 'Saved!'
        else:
            status = 'Not saved!'
            return render(request, 'todo/detailtodo.html', {'form': form, 'status': status})
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/detailtodo.html', {'todo': todo, 'form': form, 'status': status})


def closetodo(request, todo_pk):
    try:
        session = Session.objects.get(session_key=request.session.session_key)
    except Session.DoesNotExist:
        session = None
    if session is not None:
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        todo = get_object_or_404(Todo, pk=todo_pk, executor=user)
        if request.method == "POST":
            status = json.loads(request.body).get('status')
            todo.status = status
            if status in ['COMPLITED', 'FAILED']:
                todo.close_date = datetime.datetime.now()
                todo.save()
            else:
                todo.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)
