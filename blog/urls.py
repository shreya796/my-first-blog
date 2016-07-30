
from django.conf.urls import url
from . import views

#app_name='blog'



urlpatterns = [
     url(r'^$', views.post_list, name='post_list'),
   url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    #url(r'^register/$', views.registration_form, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
]




"""



urlpatterns = [
    url(r'^$', views.Indexview.as_view(), name='post_list'),

    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='post_detail'),

   url(r'^post/new/$', views.PostCreate.as_view(),name='post_new'),

    url(r'^post/(?P<pk>\d+)/edit/$',views.PostUpdate.as_view(),name='post_edit'),


    #url(r'^post/(?<pk>\d+)/delete/$',views.PostDelete.as_view(),name='post_delete'),

url(r'^register/$', views.UserFormView.as_view(), name='register'),
]

#meaning of self, empty r'^$'??

#form-template in registr.html, post_form, post_edit

"""
