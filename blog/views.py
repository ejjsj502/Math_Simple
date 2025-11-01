from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-posted_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('post-list')

# Comment create as FBV (could also be a CreateView)
@login_required
def add_comment(request, post_pk):
    """
    View para criar um comentário relacionado ao Post de id post_pk.
    Exige que o usuário esteja autenticado.
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            com = form.save(commit=False)   # não salva ainda
            com.post = post
            com.author = request.user
            com.save()
            return redirect('post-detail', pk=post_pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})

class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.order_by('-posted_at')  
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})