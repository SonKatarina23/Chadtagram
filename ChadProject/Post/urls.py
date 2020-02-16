from django.urls import path
from . import views

app_name = 'Post'

urlpatterns = [
    # Ajax stuff
    path('ajax/toggle-like', views.ToggleLike.as_view(), name='Toggle_Like'),
    path('ajax/like-post', views.LikePost.as_view(), name='Like_Post'),

    path('', views.PostList.as_view(), name='List'),
    path('p/<pk>', views.PostDetail.as_view(), name='Detail')
]
