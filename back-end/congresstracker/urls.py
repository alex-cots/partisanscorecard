"""
URL configuration for congresstracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers

from core.views import InfoViewSet, HouseRollCallViewSet, HouseViewSet, MemberDetailViewSet, SenateRollCallViewSet, SenateViewSet
from health.views import health

api_router = routers.DefaultRouter()
api_router.register('members', MemberDetailViewSet, basename='member')
api_router.register('house/(?P<congress>.+)/members', HouseViewSet, basename='house')
api_router.register('senate/(?P<congress>.+)/members', SenateViewSet, basename='senate')
api_router.register('house/(?P<congress>.+)/roll-calls', HouseRollCallViewSet, basename='house-votes')
api_router.register('senate/(?P<congress>.+)/roll-calls', SenateRollCallViewSet, basename='senate-votes')
api_router.register('info', InfoViewSet, basename='info')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('health/', health)
]
