from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^register/$',views.register),
    url(r'^register_handle/$',views.register_handle),
    url(r'^login/$',views.login),
    url(r'^check_user_name_(\w+)/$',views.check_user_name),
    url(r'^check_login/$',views.check_login),
    url(r'^session(\w+)/$',views.session),
    url(r'^verify_code/$',views.verify_code),
    url(r'^center/$',views.user_center_info),
    url(r'^site/$',views.site),
    url(r'^quit/$',views.quit),

]