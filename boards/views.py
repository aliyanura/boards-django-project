from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Boards, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone

def home(request):
    boards = Boards.objects.all()
    return render(request, 'home.html', locals())

def board_topics(request, pk):
    board = get_object_or_404(Boards, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts'))
    return render(request, 'topics.html', locals())

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Boards, pk=pk)
    if request.method=='POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk) #TODO: redirect to the created page
    else:
        form = NewTopicForm
    return render(request, 'new_topic.html', locals())

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save() 
    return render(request, 'topic_posts.html', locals())

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', locals())

@login_required
def post_edit(request, pk, topic_pk, post_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    post = get_object_or_404(Post, topic__pk=topic_pk, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = timezone.now()
            post.save()
        return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', locals())

@login_required
def post_delete(request, pk, topic_pk, post_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    post = get_object_or_404(Post, topic__pk=topic_pk, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    return render(request, 'post_delete.html', locals())