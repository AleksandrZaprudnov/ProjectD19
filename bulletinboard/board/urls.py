from django.urls import path, include
from .views import HomePageView, AdCreateView, AdUpdateView, AdDetailView,  AdListView,\
    RespOnAdCreateView, RespOnAdDetailView, RespOnAdDeleteView, AdView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('home/', HomePageView.as_view(), name='home'),
    path('board/', AdListView.as_view()),
    path('ad_create/', AdCreateView.as_view(), name='ad_create'),
    path('ad_update/<int:pk>', AdUpdateView.as_view(), name='ad_update'),
    # path('ad_detail/<int:pk>', AdDetailView.as_view(), name='ad_detail'),
    path('ad_detail/<int:pk>', AdView.as_view(), name='ad_detail'),
    path('responad_create/', RespOnAdCreateView.as_view(), name='responad_create'),
    path('responad_detail/<int:pk>', RespOnAdDetailView.as_view(), name='responad_detail'),
    path('responad_delete/<int:pk>', RespOnAdDeleteView.as_view(), name='responad_delete'),
]

