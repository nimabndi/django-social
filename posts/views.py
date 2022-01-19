from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Vote
from .forms import AddPostForm, EditPostForm, AddCommentForm, AddReplyForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_posts.html', {'posts': posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, slug=slug)
    comment = Comment.objects.filter(post=post, is_reply=False, active=True)
    reply_form = AddReplyForm()
    can_like = False
    if request.user.is_authenticated:
        if post.user_can_like(request.user):
            can_like = True
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'success')
            return redirect(post.get_absolut_url())
    else:
        form = AddCommentForm()
    return render(request, 'posts/post_detail.html',
                  {'post': post, 'comments': comment, 'form': form, 'reply': reply_form, 'can_like': can_like})


@login_required
def add_post(request, user_id):
    if request.user.id == user_id:
        if request.method == 'POST':
            form = AddPostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data['body'][:30])
                new_post.save()
                messages.success(request, 'your post submitted', 'success')
                return redirect('account:dashboard', user_id)

        else:
            form = AddPostForm()
        return render(request, 'posts/add_post.html', {'form': form})
    else:
        return redirect('posts:all_posts')


@login_required
def post_delete(request, user_id, post_id):
    if request.user.id == user_id:
        Post.objects.filter(id=post_id).delete()
        messages.success(request, 'your post deleted successfully', 'success')
        return redirect('account:dashboard', user_id)
    else:
        return redirect('posts:all_posts')


@login_required
def post_edit(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, id=post_id)
        if request.method == 'POST':
            form = EditPostForm(request.POST, instance=post)
            if form.is_valid():
                ep = form.save(commit=False)
                ep.slug = slugify(form.cleaned_data['body'[:30]])
                ep.save()
                messages.success(request, 'your post edited successfully', 'success')
                return redirect('account:dashboard', user_id)
        else:
            form = EditPostForm(instance=post)
            return render(request, 'posts/edit_post.html', {'form': form})
    else:
        return redirect('posts:all_posts')


@login_required
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.active = False
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submitted successfully', 'success')
    return redirect('posts:post_detail', post.created.year, post.created.month, post.created.day, post.slug)
    # return redirect(post.get_absolut_url())


