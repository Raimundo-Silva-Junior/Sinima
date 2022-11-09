from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Post

def home(request):
    
    return render(request, 'blog/home.html', context={"posts": Post.objects.all()})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3
    
    def get_context_data(self,**kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['active'] = 'home'
        context["Dados"] = [
            Post.objects.filter(categoria='Filmes').order_by('-date_posted'),
            Post.objects.filter(categoria='Séries').order_by('-date_posted'),
            Post.objects.filter(categoria='Animes').order_by('-date_posted')
        ]
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/base_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        
        if self.request.path == "/filmes/":
            return Post.objects.filter(categoria="Filmes").order_by('-date_posted')
        elif self.request.path == "/series/":
            return Post.objects.filter(categoria="Séries").order_by('-date_posted')
        elif self.request.path == "/animes/":
            return Post.objects.filter(categoria="Animes").order_by('-date_posted')
        else:
            user = get_object_or_404(User, username=self.kwargs.get('username'))
            return Post.objects.filter(autor=user).order_by('-date_posted')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.path == "/filmes/":
            context['title'] = "Filmes"
            context['active'] = 'Filmes'
        elif self.request.path == "/series/":
            context['title'] = "Séries"
            context['active'] = 'Séries'
        elif self.request.path == "/animes/":
            context['title'] = "Animes"
            context['active'] = 'Animes'
        else:
            context['title'] = f"Postagens de {self.kwargs.get('username')}"
        
        context['request'] = self.request.path
        return context
    
class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['título', 'categoria', 'resumo', 'conteúdo', "capa"]
    
    def form_valid(self, form):
        
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'create'
        context['title'] = "Criar Postagem"
        return context
    
    def test_func(self):

        return self.request.user.is_superuser
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Post
    fields = ['título', 'categoria', 'resumo', 'conteúdo', "capa"]
    
    def form_valid(self, form):
        
        form.instance.autor = self.request.user
        return super().form_valid(form)
        
        
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.autor:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.autor:
            return True
        return False


