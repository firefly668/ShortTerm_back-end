"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, re_path,path
from firstapp import views
from firstapp import urls
from django.views.generic import TemplateView

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('api/', include(urls)),  # vue前端获取数据的url
    re_path('^$', TemplateView.as_view(template_name="index.html")),
    path('PersonIndex/',TemplateView.as_view(template_name="index.html")),
    path('WorkRight/',TemplateView.as_view(template_name="index.html")),
    path('Test1/', TemplateView.as_view(template_name="index.html")),
    path('craftTable/<int:UID>/', TemplateView.as_view(template_name="index.html")),
    path('myDocs/<int:UID>/', TemplateView.as_view(template_name="index.html")),
    path('Edit/<int:UID>/<int:AID>/<int:MID>/', TemplateView.as_view(template_name="index.html")),
    path('Comment/', TemplateView.as_view(template_name="index.html")),
    path('Edit/<int:UID>/<int:AID>/<int:MID>/<int:TID>/', TemplateView.as_view(template_name="index.html")),
    path('myTeam/<int:UID>/<int:TID>/', TemplateView.as_view(template_name="index.html")),
    path('personalRecycleBin/<int:UID>/', TemplateView.as_view(template_name="index.html")),
    path('teamRecycleBin/<int:TID>/', TemplateView.as_view(template_name="index.html")),
    path('Test/', TemplateView.as_view(template_name="index.html")),
    path('OtherIndex/<int:UID>/', TemplateView.as_view(template_name="index.html")),
    path('sharepage/<int:UID>/<int:AID>/', TemplateView.as_view(template_name="index.html")),
    path('sharepage/<int:AID>/', TemplateView.as_view(template_name="index.html")),
    path('viewNumSider/', TemplateView.as_view(template_name="index.html")),

]
