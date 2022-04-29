from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('all/', views.AllRecordView.as_view(), name='all_record'),
    path('newWant/', views.NewWantView.as_view(), name='new_want'), 
    path('newOffer/', views.NewOfferView.as_view(), name='new_offer'), 
    path('detail/<int:record_id>/', views.DetailView.as_view(), name='detail'),
    path('', views.home, name='home'),
]