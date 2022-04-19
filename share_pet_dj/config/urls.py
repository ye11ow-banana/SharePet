from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

handler404 = 'core.service_pages.handler404'
handler400 = 'core.service_pages.handler400'

urlpatterns = [

] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    prefix_default_language=False
)
