#from pickle import GET
#from webbrowser import get
#from winreg import HKEY_PERFORMANCE_DATA
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login as loginUser ,logout
from app.forms import TODOform
from app.models import TODO
from django.contrib.auth.decorators import login_required
# Create your views here.
#decorator enchances the view
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:      # to show only the logged in user todos
        user = request.user
    form = TODOform()
    todos = TODO.objects.filter(user = user).order_by('priority')
    return render(request, 'index.html' , context = {'form': form , 'todos' : todos})




# this is for login verification
def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {"form" : form}
        return render(request, 'login.html' , context = context)
    else:
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username1 = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password')
            user = authenticate(username = username1, password = password1) # this will return the  object  
            # now we need store user info into server session
            if user is not None:
                loginUser(request,user)
                return redirect('home')
        else:
            context = {
                'form': form
            }
            return render(request,'login.html' , context = context)
 



# this is for the signup 
def signup(request):
    if request.method == 'GET':
        form = UserCreationForm
        context = {
            "form" : form
        }
        return render(request,'signup.html', context = context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            "form" : form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html' , context = context)
#decorator
@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
    form = TODOform(request.POST)
    if form.is_valid():

        print(form.cleaned_data)
        todo = form.save(commit = False)
        todo.user = user
        todo.save()

        return redirect('home')
    else:
        return render(request, 'index.html' , context = {'form': form})
    
def signout(request):
    logout(request)
    return redirect('login')

def delete_todo(request, id):
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request, id , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')
