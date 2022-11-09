from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    
    título = models.CharField(max_length=100, verbose_name='título')
    categoria = models.CharField(max_length=100,  verbose_name='categoria')
    resumo = models.TextField(verbose_name='resumo')
    conteúdo = models.TextField( verbose_name='conteúdo')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='date_posted')
    autor = models.ForeignKey(User, on_delete=models.CASCADE,  verbose_name='autor')
    capa = models.ImageField(default='default_cover.jpg', upload_to='article_imgs',  verbose_name='capa')
    
    def __str__(self):
        return self.título

    def get_absolute_url(self):
        return reverse('blog-post-detail', kwargs={'pk': self.pk})
    
    def conteúdo_split(self):
        return self.conteúdo.split('\n')
    
