from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^get/$', views.get_redir, name='get'),
    url(r'^login/$', views.login_portal().index, name='index'),
	url(r'^pass/$', views.login_portal().send_otp, name='send_otp'),
	url(r'^auth/$', views.authenticate, name='auth'),
	url(r'^error/$', views.wrongotp),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
