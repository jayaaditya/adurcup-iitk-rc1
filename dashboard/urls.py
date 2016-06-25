from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^dash/$', views.dash),
	url(r'^reboot/$',views.reboot),
	url(r'^users/$', views.allusers),
	url(r'^block/$',views.deauth),
	url(r'^check/$',views.check_state),
	url(r'^showusage/$',views.show_usage)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)