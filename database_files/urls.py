from django.conf.urls import url
from django.views.decorators.cache import cache_page
from database_files.views import serve  # , serve_thumb

urlpatterns = [
    #  url(r'^t/(?P<x>\d+)/(?P<y>\d+)/(?P<name>.+)$', serve_thumb, name='database_file_thumb'),
    url(r'^/?(?P<name>.+)$', cache_page(60 * 15)(serve), name='database_file'),
]
