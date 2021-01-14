from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import MakePost
from .forms import MakePostForm, UserCreationForm


def home(request):
    posts = MakePost.objects.order_by('-created')
    return render(request, 'simple_website/home.html',{'posts':posts})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'simple_website/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'simple_website/signupuser.html', {'form':UserCreationForm(), 'error':'Username already taken'})
        else:
            return render(request, 'simple_website/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords do not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'simple_website/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'simple_website/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def newpost(request):
    if request.method == 'GET':
        return render(request, 'simple_website/newpost.html', {'form':MakePostForm()})
    else:
        try:
            form = MakePostForm(request.POST)
            newpost = form.save(commit=False)
            newpost.user = request.user
            newpost.save()
            return redirect('home')
        except ValueError:
            return render(request, 'simple_website/newpost.html', {'form':MakePostForm(), 'error':'Bad data passed in'})


def myposts(request):
    posts = MakePost.objects.filter(user=request.user).order_by('-created')
    return render(request, 'simple_website/myposts.html',{'posts':posts})


def viewpost(request, post_pk):
    post = get_object_or_404(MakePost, pk=post_pk, user=request.user)
    if request.method == 'GET':
        form = MakePostForm(instance=post)
        return render(request, 'simple_website/viewpost.html', {'post':post, 'form':form})
    else:
        try:
            form = MakePostForm(request.POST, instance=post)
            form.save()
            return redirect('myposts')
        except ValueError:
            return render(request, 'simple_website/viewpost.html', {'post':post, 'form':form, 'error': 'Bad data passed in'} )


def deletepost(request, post_pk):
    post = get_object_or_404(MakePost, pk=post_pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('myposts')
