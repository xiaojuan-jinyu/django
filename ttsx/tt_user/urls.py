from django.conf.urls import url
import views

urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^register_handle/$',views.register_handle),
    url(r'^login/$',views.login),
    url(r'^check_user_name_(\w+)/$',views.check_user_name),
    url(r'^check_login/$',views.check_login),
    url(r'^index/$',views.index),
    url(r'^session(\w+)/$',views.session),
    url(r'^verify_code/$',views.verify_code),
    url(r'^user_center_info/$',views.user_center_info),
]