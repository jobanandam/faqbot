from django.urls import path

from . import views

app_name = 'mybot'

urlpatterns = [
    path('v1/', views.VersionOne.as_view(), name='index'),
    path('v2/', views.VersionTwo.as_view(), name='index'),
    path('v3/', views.VersionThree.as_view(), name='index'),
    path('tcs/', views.TCSVersion.as_view(), name='index'),
    path('crawler/', views.crawler_page, name='crawler'),
    path('getbotans/', views.get_human_ques, name='getbotans'),
]