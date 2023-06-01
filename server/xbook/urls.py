"""
URL configuration for xbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from api.views.download import DirectlyDownloadView
from api.views.flower import CeleryFlowerView

urlpatterns = [
    re_path(r"^r_download/(?P<file_pk>\w+)/(?P<file_id>\w+)/(?P<file_name>\S+)", DirectlyDownloadView.as_view(),
            name="r_download"),
    path('admin/', admin.site.urls),
    path("api/v1/", include('api.urls')),
    re_path(r'flower/(?P<path>.*)', CeleryFlowerView.as_view(), name='flower-view'),
    # media路径配置 开发环境可以启动下面配置，正式环境需要让nginx读取资源，无需进行转发
    re_path('^f_download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
