from django.urls import path

from .views import (HomePageView,
                    ContactPageView,
                    ErrorPageView,
                    newDetailView,
                    WorldNewsView,
                    SportNewsView,
                    TechnologyNewsView,
                    LocalNewsView,
                    NewsCreateView,
                    NewsUpdateView,
                    NewsDeleteView,
                    SearchResultsView,
                    )

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact-us/', ContactPageView.as_view(), name='contact'),
    path('404/', ErrorPageView.as_view(), name='404'),
    path('news/create/', NewsCreateView.as_view(), name='new_create'),
    path('news/<slug:news>/', newDetailView, name="new_detail"),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='new_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='new_delete'),
    path('sport/', SportNewsView.as_view(), name='sport'),
    path('dunyo/', WorldNewsView.as_view(), name='dunyo'),
    path('texnologiya/', TechnologyNewsView.as_view(), name='texnologiya'),
    path('mahalliy/', LocalNewsView.as_view(), name='mahalliy'),
    path('search-results/', SearchResultsView.as_view(), name='search_result'),
]