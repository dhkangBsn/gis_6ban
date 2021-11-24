import json

from django.contrib.auth.decorators import login_required

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin

from articleapp.decorators import article_ownership_required
from articleapp.forms import ArticleCreationForm
from articleapp.models import Article
from commentapp.forms import CommentCreationForm
import requests
import re

URL = 'http://15.164.232.127:5001/lyrics_emotion'
headers = {'User-Agent':'Mozila/5.0'}

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    # success_url = reverse_lazy('articleapp:list')
    template_name = 'articleapp/create.html'

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Foreign Key 지정하여 삽입하기 위한 코드
        return super().form_valid(form)

    def get_success_url(self):  # self.object는 target_object와 동일하다고 보면 됨
        obj = Article.objects.get(pk=self.object.id)
        session = requests.Session()
        payload = {'lyrics' : obj.content}
        session = requests.Session()
        res = session.post(URL, headers=headers, data=payload)
        result = json.loads(res.text)['emotion_score']
        result_dict = {'joy':result[0], 'sadness':result[1], 'fear':result[2], 'upset':result[3], 'anger':result[4], 'hurt':result[5]}

        obj.joy = result_dict['joy']
        obj.sadness = result_dict['sadness']
        obj.fear = result_dict['fear']
        obj.upset = result_dict['upset']
        obj.anger = result_dict['anger']
        obj.hurt = result_dict['hurt']

        obj.save()
        return reverse('articleapp:detail', kwargs={'pk': self.object.pk})


class ArticleDetailView(DetailView, FormMixin):
    model = Article
    context_object_name = 'target_article'
    template_name = 'articleapp/detail.html'
    form_class = CommentCreationForm


@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleCreationForm
    context_object_name = 'target_article'
    template_name = 'articleapp/update.html'

    def get_success_url(self):  # self.object는 target_object와 동일하다고 보면 됨
        obj = Article.objects.get(pk=self.object.id)

        session = requests.Session()
        payload = {'lyrics': obj.content}
        session = requests.Session()
        res = session.post(URL, headers=headers, data=payload)
        result = json.loads(res.text)['emotion_score']
        session.close()

        result_dict = {'joy': result[0], 'sadness': result[1], 'fear': result[2], 'upset': result[3],
                       'anger': result[4], 'hurt': result[5]}

        obj.joy = result_dict['joy']
        obj.sadness = result_dict['sadness']
        obj.fear = result_dict['fear']
        obj.upset = result_dict['upset']
        obj.anger = result_dict['anger']
        obj.hurt = result_dict['hurt']

        obj.save()
        return reverse('articleapp:detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    model = Article
    context_object_name = 'target_article'
    success_url = reverse_lazy('articleapp:list')
    template_name = 'articleapp/delete.html'


class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articleapp/list.html'
    paginate_by = 20

