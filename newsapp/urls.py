from django.urls import path

from .views import (HomePageView,
                    ContactPageView,
                    ErrorPageView,
                    newDetailView,
                    HomePageView,
                    SportNewsView,
                    WorldNewsView,
                    TechnologyNewsView,
                    LocalNewsView,
                    )

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact-us/', ContactPageView.as_view(), name='contact'),
    path('404/', ErrorPageView.as_view(), name='404'),
    path('news/<slug:news>/', newDetailView, name="new_detail"),
    path('sport/', SportNewsView.as_view(), name='sport'),
    path('dunyo/', WorldNewsView.as_view(), name='dunyo'),
    path('texnologiya/', TechnologyNewsView.as_view(), name='texnologiya'),
    path('mahalliy/', LocalNewsView.as_view(), name='mahalliy'),
]