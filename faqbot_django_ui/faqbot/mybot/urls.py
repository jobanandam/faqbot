from django.urls import path

from . import views

app_name = 'mybot'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('save/', views.get_human_ques, name='save'),
]