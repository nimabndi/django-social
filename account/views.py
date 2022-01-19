from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegisterForm, EditProfileForm, PhoneLoginForm, VerifyCodeForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.models import Post
from random import randint
from kavenegar import *
import ghasedak
from .models import Profile, Relation
from django.http import JsonResponse
from posts.models import Vote


def user_login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if next:
                    return redirect(next)
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'wrong username or password', 'warning')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            messages.success(request, 'you registered successfully', 'success')
            return redirect('posts:all_posts')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'you logged out successfully', 'success')
    return redirect('posts:all_posts')


@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    is_following = False
    relation = Relation.objects.filter(from_user=request.user, to_user=user)
    if relation.exists():
        is_following = True
    self_dash = False
    if request.user.id == user_id:
        self_dash = True
    return render(request, 'account/dashboard.html',
                  {'user': user, 'posts': posts, 'self_dash': self_dash, 'is_following': is_following})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            messages.success(request, 'your profile edited successfully', 'success')
            return redirect('account:dashboard', user_id)
    else:
        form = EditProfileForm(instance=user.profile, initial={'email': request.user.email,
                                                               'first_name': request.user.first_name,
                                                               'last_name': request.user.last_name})
    return render(request, 'account/edit_profile.html', {'form': form})


def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            global phone, rand_num
            phone = f"0{form.cleaned_data['phone']}"
            rand_num = randint(1000, 9999)
            api = KavenegarAPI(
                '707459616A52666E676E45443939433549793157646A695039727A434167424543424357714A356D7166513D')
            params = {'sender': '', 'receptor': phone, 'message': rand_num}
            api.sms_send(params)
            return redirect('account:verify')
    else:
        form = PhoneLoginForm()
    return render(request, 'account/phone_login.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if rand_num == form.cleaned_data['code']:
                profile = get_object_or_404(Profile, phone=phone)
                user = get_object_or_404(User, profile__id=profile.id)
                login(request, user)
                messages.success(request, 'logged in successfully', 'success')
                return redirect('posts:all_posts')
            else:
                messages.warning(request, 'your code is wrong', 'warning')
                return render(request, 'account/verify.html', {'form': form})
    else:
        form = VerifyCodeForm()
        if 'Referer' in request.headers.keys():
            return render(request, 'account/verify.html', {'form': form})
        else:
            return redirect('account:phone_login')


# else:
#     redirect('account:phone_login')

@login_required
def change_password(request, user_id):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, id=user_id)
            newpassword = form.cleaned_data['NewPassword']
            user.set_password(newpassword)
            user.save()
            messages.success(request, 'your password changed successfully', 'success')
            return redirect('posts:all_posts')
    else:
        form = ChangePasswordForm()
    return render(request, 'account/change_password.html', {'form': form})


@login_required
def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, id=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status': 'exists'})
        else:
            Relation(from_user=request.user, to_user=following).save()
            return JsonResponse({'status': 'ok'})


def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, id=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'notexists'})


@login_required
def post_like(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        check_vote = Vote.objects.filter(user=request.user, post=post)
        if check_vote.exists():
            # check_vote.delete()
            return JsonResponse({'status': 'exists'})
        else:
            Vote(user=request.user, post=post).save()
            return JsonResponse({'status': 'ok'})


def post_dislike(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        check_vote = Vote.objects.filter(post=post, user=request.user)
        if check_vote.exists():
            check_vote.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'notexists'})


def user_follower(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = user.following.all()
    return render(request, 'account/user_follower.html', {'followers': followers})


def User_following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followings = user.follower.all()
    return render(request, 'account/user_following.html', {'followings': followings})
