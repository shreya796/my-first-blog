
from django.conf.urls import url
from . import views

#app_name='blog'

urlpatterns =[
     url(r'^$', views.post_list, name='post_list'),

     url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),

    url(r'^post/(?P<pk>\d+)/detail/$', views.post_poem, name='post_poem'),

    url(r'^post/new/$', views.post_new, name='post_new'),

    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),

    url(r'^register/$', views.register , name='register'),

    url(r'^logout_view/$', views.logout_view, name='logout_view'),

    url(r'^login_user/$', views.login_user, name='login_user'),


    #here pk is used so that every page opened can have its own primary key
    #the pk is allotted by default




  #  url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),


#url(r'^drafts/$',views.post_draft_list,name='post_draft_list'),

#url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
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
