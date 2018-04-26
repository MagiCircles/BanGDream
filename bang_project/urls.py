from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
import api.views as api_views
from django.conf.urls import handler500, handler403

handler500 = 'magi.views.handler500'
handler403 = 'magi.views.handler403'

router = routers.DefaultRouter()

router.register(r'members', api_views.MemberViewSet)
router.register(r'memberids', api_views.MemberIDViewSet)
router.register(r'cards', api_views.CardViewSet)
router.register(r'cardids', api_views.CardIDViewSet)
router.register(r'events', api_views.EventViewSet)

urlpatterns = patterns('',
    url(r'^', include('magi.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)
