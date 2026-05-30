from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
