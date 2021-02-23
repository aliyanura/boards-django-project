from django.urls import path
from boards.views import reply_topic, post_delete, BoardsListView, BoardDetailView, NewTopicView, PostListView, PostEditView

urlpatterns = [
    # path('home/', home, name='home'),
    # path('board/<int:pk>/', board_topics, name='board_topics'),
    # path('board/<int:pk>/new/', new_topic, name='new_topic'),
    # path('board/<int:pk>/<int:topic_pk>/', topic_posts, name='topic_posts'),
    # path('board/<int:pk>/topics/<int:topic_pk>/<int:post_pk>/edit/', post_edit, name='post_edit'),
    path('home/', BoardsListView.as_view(), name='home'),
    path('board/<int:pk>/', BoardDetailView.as_view(), name='board_topics'),
    path('board/<int:pk>/new/', NewTopicView.as_view(), name='new_topic'),
    path('board/<int:pk>/topics/<int:topic_pk>/', PostListView.as_view(), name='topic_posts'),
    path('board/<int:pk>/topics/<int:topic_pk>/post/<int:post_pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('board/<int:pk>/topics/<int:topic_pk>/reply/', reply_topic, name='reply_topic'),
    path('board/<int:pk>/topics/<int:topic_pk>/post/<int:post_pk>/delete/', post_delete, name='post_delete'),

    # path('new_post/', NewPostView.as_view(), name='new_post'),
]