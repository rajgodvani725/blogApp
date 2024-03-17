# views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Blog
from django.contrib.auth.decorators import login_required
import json
from django.http import request

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        username_status = User.objects.filter(username=username).exists()
        email_status = User.objects.filter(email=email).exists()
        if username_status:
            return JsonResponse({"error": "Username already exists"}, status=400)
        if email_status:
            return JsonResponse({"error": "Email already exists"}, status=400)
        if password1 == password2:
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password1,
            )
            return JsonResponse({"message": "User registered successfully"}, status=201)
        else:
            return JsonResponse({"error": "Passwords do not match"}, status=400)
    else:
        return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.get(email=email)
        if not user:
            return JsonResponse({"error": "User not found"}, status=500)
        user = authenticate(username=user.username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"error": "Invalid email or password"}, status=500)
    else:
        return render(request, "login.html")


def home(request):
    return render(request, "home.html")


def signout(request):
    logout(request)
    return render(request, "home.html")


def emailLogin(request):
    return render(request, "email-login.html")


@csrf_exempt
@login_required(login_url="/signin/")
def publish_blog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        id = request.POST.get("id",None)
        if not id:
            is_draft = json.loads(request.POST.get("is_draft"))
            is_published = json.loads(request.POST.get("is_published"))
            Blog.objects.create(
            author=request.user,
            title=title,
            content=content,
            is_draft=is_draft,
            is_published=is_published,
        )
            return JsonResponse({"success": True})
        else:
            request_for = request.POST.get("request_for")
            if request_for =='update_blog':
                blog = Blog.objects.get(id=id)
                blog.title = title
                blog.content = content
                blog.save()
                blogs = Blog.objects.filter(author=request.user)
                serialized_blogs = [blog.to_dict() for blog in blogs]
                return JsonResponse({"blogs": serialized_blogs},status=200)
            
            if request_for == 'delete_blog':
                blog = Blog.objects.get(id=id)
                blog.delete()
                blogs = Blog.objects.filter(author=request.user)
                serialized_blogs = [blog.to_dict() for blog in blogs]
                return JsonResponse({"blogs": serialized_blogs},status=200)
            
            if request_for == 'publish_blog':
                import pdb;pdb.set_trace()
                blog = Blog.objects.get(id=id)
                blog.is_published = True
                blog.is_draft = False
                blog.save()
                blogs = Blog.objects.filter(author=request.user)
                serialized_blogs = [blog.to_dict() for blog in blogs]
                return JsonResponse({"blogs": serialized_blogs},status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
@login_required(login_url="/signin/")
def get_blogs(request):
    if request.method == "POST":
        blogs = Blog.objects.filter(is_published=True)
        serialized_blogs = [blog.to_dict() for blog in blogs]
        return JsonResponse({"blogs": serialized_blogs}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
@login_required(login_url="/signin/")
def showblog(request,id):
    blog = Blog.objects.get(id=id)
    return render(request,template_name="showblog.html", context={"blog": blog.to_dict()}, status=200)

@csrf_exempt
@login_required(login_url="/signin/")
def createblog(request):
    if request.user.is_authenticated:
        return render(request, "create-blog.html")
    else:
        return redirect("signin")
    
@csrf_exempt
@login_required(login_url="/signin/")
def myBlogs(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(author=request.user)
        serialized_blogs = [blog.to_dict() for blog in blogs]
        context = {"blogs": serialized_blogs}
        return render(request, "myblogs.html", context)
    else:
        return redirect("signin")
