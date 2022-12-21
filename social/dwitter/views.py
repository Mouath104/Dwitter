from unittest import loader
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile,Dweet,Comment
from django.http import HttpResponse,HttpResponseRedirect
from .forms import DweetForm
# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# def dashboard(request):
#     if request.method == "POST":
#         form = DweetForm(request.POST)
#         if form.is_valid():
#             dweet = form.save(commit=False)
#             dweet.user = request.user
#             dweet.save()
#     form = DweetForm()
#     return render(request, "dwitter/dashboard.html", {"form": form})

def dashboard(request):
    if request.user.is_authenticated:
        form = DweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                dweet = form.save(commit=False)
                dweet.user = request.user
                dweet.save()
                return redirect("dwitter:dashboard")
        followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
        ).order_by("-created_at")
    #comments
        return render(
        request,
        "dwitter/dashboard.html",
        {"form": form, "dweets": followed_dweets},
        )
    else:
        return HttpResponseRedirect("http://127.0.0.1:8000/user_login")

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def profile(request, pk):

    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()
        
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile #casuse it's one - to - one
        data = request.POST
        action = data.get("follow")
        
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
            current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})

def add_comment(req):
    idweet=Dweet.objects.get(id=req.POST["dweet"])
    iuser=req.user
    comment=Comment(body=req.POST["comment-body"],user=iuser,dweet=idweet)
    comment.save()
    # return render(req, "dwitter/dashboard")
    return redirect("dwitter:dashboard")
# def follow(req,id):
#     profile = Profile(user=)
#     profile.follows=req.user.id
#     profile.save()
#     return redirect(f"http://127.0.0.1:8000/profile/{id}")

def user_login(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect('http://127.0.0.1:8000/')
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect('http://127.0.0.1:8000/')
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'reg/index_login.html', {})
        # return render(request, 'reg/login.html', {})

def user_logout(request):
    if(request.user.is_authenticated):
        logout(request)
        return HttpResponseRedirect("http://127.0.0.1:8000/user_login")
    else:
        template = loader.get_template('sorry.html')
        msg="you aren't logged in yet to log out 7abib :)"
        context = {
            'msg': msg,
        }
        return HttpResponse(template.render(context, request))