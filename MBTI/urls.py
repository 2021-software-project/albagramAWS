from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from django.conf.urls import(handler404)
from .view import page_not_found_page

router = routers.DefaultRouter()


urlpatterns = [
    url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
    url(r'^(main)/', TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(login)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(mypage)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(firstulike)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(Mbti_rcm)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(mbti_result)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(Personal_rcm)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(personal_result)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(GoodBad_list)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(Alba_rating)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(Rating_list)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(information)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url(r'^(error)/',TemplateView.as_view(template_name='index.html'), name='route'),
    url('user/password-reset/:uid/:token',TemplateView.as_view(template_name='index.html'), name='index'),

    path('user/', include('user.urls')),
    path('user/admin/', admin.site.urls),
]
handler404 = page_not_found_page