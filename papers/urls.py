from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_paper, name='upload_paper'),
    path('manage/', views.manage_dashboard, name='manage_dashboard'),
    path('manage/login/', views.manage_login, name='manage_login'),
    path('manage/logout/', views.manage_logout, name='manage_logout'),
    path('manage/topic/add/', views.manage_topic_add, name='manage_topic_add'),
    path('manage/topic/<slug:slug>/edit/', views.manage_topic_edit, name='manage_topic_edit'),
    path('manage/topic/<slug:slug>/delete/', views.manage_topic_delete, name='manage_topic_delete'),
    path('manage/scrape/', views.manage_scrape, name='manage_scrape'),
    path('manage/generate/', views.manage_generate, name='manage_generate'),
]
