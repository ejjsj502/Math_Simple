from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category

# Listagem
def post_list(request):
    posts = Post.objects.order_by('-posted_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

# Detalhe
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# Criar sem form (sem validação)
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        p = Post.objects.create(title=title, content=content)
        # se quiser setar categorias via checkbox: omitted (simples)
        return redirect('post-detail', pk=p.pk)
    # template simples: usar um formulário HTML direto no template
    from django import forms
    class DummyForm(forms.Form):
        title = forms.CharField()
        content = forms.CharField(widget=forms.Textarea)
    form = DummyForm()
    return render(request, 'blog/post_form.html', {'form': form})

# Editar sem form
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post-detail', pk=post.pk)
    # reuse form as above - prepopulate
    from django import forms
    class DummyForm(forms.Form):
        title = forms.CharField()
        content = forms.CharField(widget=forms.Textarea)
    form = DummyForm(initial={'title': post.title, 'content': post.content})
    return render(request, 'blog/post_form.html', {'form': form})

# Remover com confirmação
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post-list')
    return render(request, 'blog/confirm_delete.html', {'object': post})

# Comentário (simple)
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        # exigir login? aqui assumimos usuário já autenticado
        Comment.objects.create(post=post, author=request.user, text=text)
        return redirect('post-detail', pk=post_pk)
    return render(request, 'blog/comment_form.html', {'post': post})

# Categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.order_by('-posted_at')
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})
