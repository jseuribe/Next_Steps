from django.conf.urls import url
from . import views #import the functions in views.py of ns

app_name = 'ns'
urlpatterns = [
	url(r'^login/$', views.login, name='login'),
	url(r'^home/$', views.index, name='index')
]