from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Boards, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# def home(request):
#     boards = Boards.objects.all()
#     return render(request, 'home.html', locals())

class BoardsListView(ListView):
    model = Boards
    template_name = 'home.html'
    context_object_name = 'boards'

# def board_topics(request, pk):
#     board = get_object_or_404(Boards, pk=pk)
#     topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts'))
#     return render(request, 'topics.html', locals())

class BoardDetailView(DeleteView):
    model = Boards
    template_name = 'topics.html'
    context_object_name = 'board'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = self.get_object().topics.order_by('-last_updated').annotate(replies=Count('posts'))
        return context

# @login_required
# def new_topic(request, pk):
#     board = get_object_or_404(Boards, pk=pk)
#     if request.method=='POST':
#         form = NewTopicForm(request.POST)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.starter = request.user
#             topic.save()
#             post = Post.objects.create(
#                 message = form.cleaned_data.get('message'),
#                 topic = topic,
#                 created_by = request.user
#             )
#             return redirect('topic_posts', pk=pk, topic_pk=topic.pk) #TODO: redirect to the created page
#     else:
#         form = NewTopicForm
#     return render(request, 'new_topic.html', locals())


class NewTopicView(CreateView, LoginRequiredMixin):
    model = Topic
    template_name = 'new_topic.html'
    form_class = NewTopicForm
    context_object_name = 'form'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board']=Boards.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        topic = form.save(commit=False)
        board_pk = self.kwargs.get('pk')
        topic.board = Boards.objects.get(pk=self.kwargs.get('pk'))
        topic.starter = self.request.user
        topic.save()
        post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = self.request.user)
        return redirect('topic_posts', pk=board_pk, topic_pk=topic.pk)


# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save() 
#     return render(request, 'topic_posts.html', locals())

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board_id=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic']= self.topic
        self.topic.views += 1
        self.topic.save()
        return context



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

# @login_required
# def post_edit(request, pk, topic_pk, post_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     post = get_object_or_404(Post, topic__pk=topic_pk, pk=post_pk)
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.updated_at = timezone.now()
#             post.save()
#         return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
#     else:
#         form = PostForm()
#     return render(request, 'post_edit.html', locals())


class PostEditView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post'
    fields = ('message', )
    pk_url_kwarg = 'post_pk'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


@login_required
def post_delete(request, pk, topic_pk, post_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    post = get_object_or_404(Post, topic__pk=topic_pk, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    return render(request, 'post_delete.html', locals())

def new_post(request):
    if request.method=='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {})


# class NewPostView(View):
#     def render(self, request):
#         return render(request, 'new_post.html', {'form': form})

#     def post(self, request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         return self.render(request)

#     def get(self, request):
#         form = PostForm()
#         return self.render(request)