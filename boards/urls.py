from django.urls import path
from boards.views import home, board_topics, new_topic, topic_posts, reply_topic, post_edit, post_delete

urlpatterns = [
    path('home/', home, name='home'),
    path('board/<int:pk>/', board_topics, name='board_topics'),
    path('board/<int:pk>/new/', new_topic, name='new_topic'),
    path('board/<int:pk>/<int:topic_pk>/', topic_posts, name='topic_posts'),
    path('board/<int:pk>/topics/<int:topic_pk>/<int:post_pk>/edit/', post_edit, name='post_edit'),
    path('board/<int:pk>/topics/<int:topic_pk>/reply/', reply_topic, name='reply_topic'),
    path('board/<int:pk>/topics/<int:topic_pk>/<int:post_pk>/delete/', post_delete, name='post_delete'),
]