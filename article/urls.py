from django.urls import path
from article import views

app_name = 'article'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
]
