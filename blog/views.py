from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from blog.models import Post, Comment
from django.http import HttpResponseRedirect
from .forms import CommentForm, PostForm
from django.views.generic.edit import UpdateView


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Modificado para usar get_object_or_404
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog/detail.html", context)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Primeiro, salva o formulário, mas commit=False diz para não enviar para o banco de dados ainda
            post = form.save(commit=False)
            post.save()  # Salva o post no banco de dados
            form.save_m2m()  # Salva as relações ManyToMany
            return redirect('blog_index')  # Redireciona para a página inicial após o sucesso
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit_form.html'  # Um novo template para edição
    success_url = reverse_lazy('index')  # Redireciona para a página inicial após o sucesso