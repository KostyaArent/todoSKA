from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
import datetime

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
    todos = Todo.objects.filter(executor=request.user, close_date__isnull=True)
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
