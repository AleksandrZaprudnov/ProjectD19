from django.urls import path
from .views import HomePageView, AdCreateView, AdUpdateView,  AdListView,\
    RespOnAdCreateView, RespOnAdDetailView, RespOnAdListView, RespOnAdDeleteView,\
    AdView, MediaContentCreateView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('home/', HomePageView.as_view(), name='home'),
    path('board/', AdListView.as_view()),
    path('responad/', RespOnAdListView.as_view(), name='responad_list'),
    path('ad_create/', AdCreateView.as_view(), name='ad_create'),
    path('ad_update/<int:pk>', AdUpdateView.as_view(), name='ad_update'),
    path('ad_detail/<int:pk>', AdView.as_view(), name='ad_detail'),
    path('responad_create/', RespOnAdCreateView.as_view(), name='responad_create'),
    path('responad_detail/<int:pk>', RespOnAdDetailView.as_view(), name='responad_detail'),
    path('responad_delete/<int:pk>', RespOnAdDeleteView.as_view(), name='responad_delete'),
    path('mediacontent_create/', MediaContentCreateView.as_view(), name='mediacontent_create'),
]

