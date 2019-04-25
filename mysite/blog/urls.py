from django.urls import path, re_path
from blog import views

app_name ='blog'

urlpatterns= [
	path('', views.PostListView.as_view(), name='post_list'),
	path('about/', views.AboutView.as_view(), name='about'),
	re_path(r'post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
	path('post/new/', views.PostCreateView.as_view(), name='post_new'),
	re_path(r'post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
	re_path(r'post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
	path('draft/', views.DraftListView.as_view(), name='draft_list'),
	re_path(r'post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='post_comment'),
	re_path(r'comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
	re_path(r'comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
	re_path(r'post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
	re_path(r'post/(?P<pk>\d+)/unpublish/$', views.post_unpublish, name='post_unpublish'),
]