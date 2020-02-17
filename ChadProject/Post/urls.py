from django.urls import path
from . import views

app_name = 'Post'

urlpatterns = [
    # Ajax stuff
    path('ajax/toggle-like', views.ToggleLike.as_view(), name='Toggle_Like'),
    path('ajax/like-post', views.LikePost.as_view(), name='Like_Post'),

    path('p/add-comment', views.AddComment.as_view(), name='Add_Comment'),
    path('comment/<pk>/delete-comment', views.DeleteComment.as_view(), name='Delete_Comment'),

    path('', views.PostList.as_view(), name='List'),
    path('p/<pk>/update', views.UpdatePost.as_view(), name='Update'),
    path('p/<pk>/delete', views.DeletePost.as_view(), name='Delete'),
    path('p/create-post', views.CreatePost.as_view(), name='Create'),
    path('p/<pk>', views.PostDetail.as_view(), name='Detail')
]
