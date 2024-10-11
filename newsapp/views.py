from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import ContactForm
from .models import News, Category
from newsproject.custom_user_passes import CustomUserPassesMixin
from .forms import CommentForm
from django.urls import reverse


# Create your views here.


class HomePageView(ListView):
    model = News
    template_name = "home.html"
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.objects.all().order_by('-publish_time')[:5]
        context['images'] = News.objects.all().order_by('-publish_time')[:6]
        context['local_one'] = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[:1]
        context['local_news'] = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[1:6]
        context['world_news'] = News.published.all().filter(category__name='Dunyo').order_by('-publish_time')[:6]
        context['sport_news'] = News.published.all().filter(category__name='Sport').order_by('-publish_time')[:6]
        context['technology_news'] = News.published.all().filter(category__name='Texnologiya').order_by(
            '-publish_time')[:6]
        return context


def newDetailView(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # Hitcount
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {"pk": hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = news.comments.filter(active=True).count()
    new_comment = None
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.new = news
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('new_detail', args=[news.slug]))
    context = {
        "news": news,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "comment_count": comment_count
    }
    return render(request, 'new_detail.html', context)


class SearchResultsView(ListView):
    model = News
    template_name = 'search_results.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query))


class ContactPageView(TemplateView):
    template_name = "contact.html"

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur</h2>")
        context = {
            "form": form
        }
        return render(request, "contact.html", context)


class ErrorPageView(TemplateView):
    template_name = "404.html"


class SportNewsView(ListView):
    model = News
    template_name = 'sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news


class WorldNewsView(ListView):
    model = News
    template_name = 'dunyo.html'
    context_object_name = 'world_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Dunyo')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'texnologiya.html'
    context_object_name = 'technology_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class LocalNewsView(ListView):
    model = News
    template_name = 'mahalliy.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news


class NewsUpdateView(CustomUserPassesMixin, UpdateView):
    model = News
    fields = ('title', 'body', 'category', 'image',)
    template_name = 'crud/news_edit.html'


class NewsDeleteView(CustomUserPassesMixin, DeleteView):
    model = News
    success_url = reverse_lazy('home')
    template_name = 'crud/news_delete.html'


class NewsCreateView(CustomUserPassesMixin, CreateView):
    model = News
    fields = ('title', 'title_uz', 'title_en', 'title_ru',
              'slug', 'body', 'body_uz', 'body_en', 'body_ru',
              'image', 'category', 'status',)
    template_name = 'crud/news_create.html'

