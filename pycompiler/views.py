from pycompiler.models import Snippet
import sys

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import SnippetForm

# Create your views here.

def home(request):
    return render(request, 'pycompiler/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'pycompiler/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(request, 'pycompiler/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'pycompiler/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'pycompiler/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'pycompiler/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('/')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def yo(request):
    return render(request,'pycompiler/test.html')

@login_required
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {'form':SnippetForm()})
    else:
        try:
            form = SnippetForm(request.POST)

            #Compilation 
            code_part = request.POST['text']
            input_part = request.POST['input']
            if code_part == "None":
                return render(request, 'index.html', {'form':SnippetForm(), 'error':'Bad data passed in. Try again.'})
            fn = request.POST['filename']
            if fn == "None":
                error = "Warning !! No file name given "
            y = input_part
            input_part = input_part.replace("\n"," ").split(" ")
            # print(input_part)
            def input():
                a = input_part[0]
                del input_part[0]
                return a
            try:
                orig_stdout = sys.stdout
                sys.stdout = open('file.txt', 'w')
                # print("before",input_part)
                exec(code_part,{'input': input})
                # print("after",input_part)

                sys.stdout.close()
                sys.stdout=orig_stdout
                output = open('file.txt', 'r').read()

            except Exception as e:
                sys.stdout.close()
                sys.stdout=orig_stdout
                output = e
            print(output)
            newsnippet = form.save(commit=False)
            newsnippet.user = request.user
            newsnippet
            newsnippet.save()
            initial = { "filename":request.POST['filename'], "text":request.POST['text'],"input":request.POST['input'],"output":output}
            return render(request, 'index.html', {'form':SnippetForm(initial=initial),'error':error})
        except ValueError:
            return render(request, 'index.html', {'form':SnippetForm(), 'error':'Bad data passed in. Try again.'})



@login_required
def viewcode(request, code_pk):
    code = get_object_or_404(Snippet, pk=code_pk, user=request.user)
    if request.method == 'GET':
        form = SnippetForm(instance=code)
        return render(request, 'index.html', {'form':form})
    else:
        try:
            form = SnippetForm(request.POST,instance=code)

            #Compilation 
            code_part = request.POST['text']
            input_part = request.POST['input']
            y = input_part
            input_part = input_part.replace("\n"," ").split(" ")
            def input():
                a = input_part[0]
                del input_part[0]
                return a
            try:
                orig_stdout = sys.stdout
                sys.stdout = open('file.txt', 'w')
                exec(code_part)
                sys.stdout.close()
                sys.stdout=orig_stdout
                output = open('file.txt', 'r').read()

            except Exception as e:
                sys.stdout.close()
                sys.stdout=orig_stdout
                output = e
            print(output)
            newsnippet = form.save(commit=False)
            newsnippet.user = request.user
            newsnippet
            newsnippet.save()
            initial = { "filename":request.POST['filename'], "text":request.POST['text'],"input":request.POST['input'],"output":output}
            return render(request, 'index.html', {'form':SnippetForm(initial=initial)})
        except ValueError:
            return render(request, 'index.html', {'form':SnippetForm(), 'error':'Bad data passed in. Try again.'})


def savedcodes(request):
    codes= Snippet.objects.filter(user=request.user)
    return render(request, 'pycompiler/saved.html', {'codes':codes})