from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "error_resolve_app"
urlpatterns = [
    
    path('', TemplateView.as_view(template_name='error_resolve_app/home.html'), name='home'),
    path('my_article/', views.GetMyArticle.as_view(), name="my_article"),
    path('article_upload/', TemplateView.as_view(template_name='error_resolve_app/article_upload.html'), name='article_upload'),
    path('article_save/', views.ArticleSave.as_view(), name='article_save'),
    path('detail_article/', views.GetDetailArticle.as_view(), name="detail_article"),
    path("article_show/<int:article_id>/", views.ArticleShowView.as_view(), name="article_show"),
    path("article_search/", TemplateView.as_view(template_name='error_resolve_app/article_search.html'), name='search'),
    path("result_articles/", views.GetResultArticles.as_view(), name="result_articles"),
    
]
