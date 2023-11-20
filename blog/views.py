from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from blog.models import Post, Comment, Category
from .forms import CommentForm, PostForm
from django.views.generic.edit import UpdateView, CreateView, DeleteView


class BlogIndexView(ListView):
    model = Post
    template_name = 'blog/index.html'  # Caminho do template para a lista de posts
    context_object_name = 'posts'  # Nome do contexto a ser usado no template
    ordering = ['-created_on']  # Ordem dos posts


class AllCategoriesListView(ListView):
    model = Category
    template_name = 'blog/all_categories.html'


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'  # Caminho do template para categorias
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(categories__name__contains=self.kwargs['category']).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_on')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user  # Atribuir o usuário, se necessário
            comment.save()
            return redirect('blog_detail', pk=self.object.pk)

        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'  # Caminho do template para criar posts
    success_url = reverse_lazy('blog_index')  # Redireciona para a página inicial após o sucesso

    def form_valid(self, form):
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit_form.html'
    success_url = reverse_lazy('index')  # Redireciona para a página inicial após o sucesso


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Template para confirmação de exclusão
    success_url = reverse_lazy('blog_index')  # Redireciona após excluir o post
