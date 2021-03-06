from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView)
from django.utils import timezone
from blog_app.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from blog_app.forms import CommentForm, ProfileForm, PostForm
from blog_site.blog_app.models import Profile


class CreateProfileView(CreateView):
    '''The view to create an account/profile.'''
    model = Profile
    form_class = ProfileForm

class DeleteProfileView(LoginRequiredMixin, DeleteView):
    '''The view to  delete an account/profile.'''
    login_url = '/login/'
    model = Profile
    form_class = ProfileForm

class AboutView(TemplateView):
    '''The view for the about page.'''
    template_name = 'about.html'

class PostListView(ListView):
    '''The view for the series of posts made.'''
    model = Post

    # Formats how the list of posts should appear on the website in terms of date and order.
    def get_queryset(self):
        return Post.objects.filter(date_published__lte=timezone.now()).order_by('-date_published')

class PostDetailView(DetailView):
    '''The view that provides the details of a post.'''
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    '''The view to create a post.'''
    login_url = '/login/' # The url the user is directed to in case they are not logged in.
    form_class =  PostForm
    model = Post

class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''The view to update an existing post.'''
    login_url = '/login/'
    form_class = PostForm
    model = Post

class DeletePostView(LoginRequiredMixin, DeleteView):
    '''Deletes a post from the website.'''
    login_url = '/login/'
    model = Post
    success_url = reverse_lazy('blog_app:post_list')

class DraftListView(LoginRequiredMixin, ListView):
    '''The view to get the list of drafts you have.'''
    model = Post
    login_url = '/login/'

    def get_queryset(self):
        return Post.objects.filter(date_published___isnull=True).order_by('-date_created')

###################
#     COMMENT     #
###################
@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog_app:post_list', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save(commit=False)
            comment_form.post = post
            comment_form.save()
            return redirect('blog_app:detail', pk=comment_form.post.pk)
    else:
        form = CommentForm()
    return render(request, '../blog_app/templates/blog_app/comment_form.html', context={'form':form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog_app:post_detail', pk=post_pk)