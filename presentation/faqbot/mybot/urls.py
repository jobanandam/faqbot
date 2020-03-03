from django.urls import path

from . import views

app_name = 'mybot'

urlpatterns = [
    path('v1/', views.VersionOne.as_view(), name='index'),
	path('v2/', views.VersionTwo.as_view(), name='index'),
    path('v3/', views.VersionThree.as_view(), name='index'),
    path('getbotans/', views.get_human_ques, name='getbotans'),
]