from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import ContactForm
from .models import News, Category


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
    context = {
        "news": news
    }
    return render(request, 'new_detail.html', context)


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

