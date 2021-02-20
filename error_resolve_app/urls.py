from django.urls import path
from . import views

app_name = "error_resolve_app"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("upload/", views.ArticleUploadView.as_view(), name="upload"),
    path("article_show/<int:article_id>/", views.ArticleShow.as_view(), name="article_show"),
    
]
