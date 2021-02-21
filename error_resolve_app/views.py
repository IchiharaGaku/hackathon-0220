from django.shortcuts import render, redirect
from django.views import View
from .models import Article
from django.core.files.storage import default_storage, FileSystemStorage
from django.conf import settings
import ffmpeg
import json
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
DATA_DIR = settings.MEDIA_ROOT

# 自分が書いた記事をとってくる
class GetMyArticle(View):
    def get(self, request, *args, **kwargs):
        data = {}
        my_articles = Article.objects.filter(upload_user__id=request.user.id).values(
            "id",
            "movie_name",
            "content",
            "created_at",
            "title",
            "upload_user__username",
            "upload_user__id",
        )
        data["user"] = {"username": request.user.username}
        data["my_articles"] = list(my_articles)
       
        
        return JsonResponse(data, safe=False)




# 記事の投稿
class ArticleSave(View):
    def post(self, request, *args, **kwargs):

        upload_file_name = request.FILES["file"].name  # ファイル名
        movie = request.FILES["file"]  # ファイルの中身
        content = request.POST["content"]
        title = request.POST["title"]

        new_article = Article()
        new_article.upload_file_name = upload_file_name
        new_article.content = content
        new_article.title = title
        new_article.created_at = timezone.now()
        new_article.upload_user = request.user
        new_article.save()

        try:
            storage = FileSystemStorage()
            storage.location = DATA_DIR + "/" + str(new_article.id)
            file_name = storage.save(upload_file_name, movie)

            self.make_video_thumb(
                DATA_DIR + "/" + str(new_article.id) + "/" + file_name,
                new_article.thumb_frame,
                DATA_DIR + "/" + str(new_article.id) + "/thumb.jpg",
            )

        except:
            self.delete_video(new_article.id, file_name)
            new_article.delete()
            raise

        else:
            new_article.movie_name = file_name
            new_article.save()

        my_articles = Article.objects.all().values()
        return JsonResponse(list(my_articles), safe=False)

    def make_video_thumb(self, src_filename, capture_frame, dst_filename=None):

        probe = ffmpeg.probe(src_filename)
        video_info = next(x for x in probe["streams"] if x["codec_type"] == "video")
        nframes = video_info["nb_frames"]
        avg_frame_rate = (lambda x: int(x[0]) / int(x[1]))(
            video_info["avg_frame_rate"].split("/")
        )
        print(avg_frame_rate)
        start_position = int(capture_frame) / avg_frame_rate

        if dst_filename == None:
            out_target = "pipe:"
        else:
            out_target = dst_filename

        im = (
            ffmpeg.input(src_filename, ss=start_position, t=1)
            .filter("scale", 200, -1)
            .output(
                out_target,
                vframes=1,
                format="image2",
                vcodec="mjpeg",
                qscale=1,
                loglevel="warning",
            )
            .overwrite_output()
            .run(capture_stdout=True)
        )

        return im

    def delete_video(self, content_id, video_filename):

        print("remove files at " + str(content_id) + "/")
        storage = FileSystemStorage()
        storage.location = DATA_DIR
        storage.delete(str(content_id) + "/" + video_filename)
        storage.delete(str(content_id) + "/" + "thumb.jpg")
        storage.delete(str(content_id) + "/")


# 記事詳細画面を表示させるためのクラス
class ArticleShowView(View):
    def get(self, request, article_id, *args, **kwargs):

        request.session["article_id"] = article_id

        return render(request, "error_resolve_app/article_show.html")


# 記事詳細のデータをとってくる

class SearchResultArticles(View):
    def get(self, request, *arags, **kwargs):

        request.session["keyword"] = request.GET["keyword"]
        return render(request, "error_resolve_app/article_result.html")

# keywordがtitleに含まれている記事をとってくる
class GetResultArticles(View):
    def get(self, request, *args, **kwargs):

        keyword = request.session["keyword"]
        result_articles = Article.objects.filter(title__icontains=keyword).values(
            "id",
            "movie_name",
            "content",
            "created_at",
            "title",
            "upload_user__username",
            "upload_user__id",
        )
        print(result_articles)
        return JsonResponse(list(result_articles), safe=False)

       
class GetDetailArticle(View):
    def get(self, request, *args, **kwargs):

        article_id = request.session["article_id"]
        article = Article.objects.get(pk=article_id)
        article_info = Article.objects.values(
            "id",
            "movie_name",
            "content",
            "created_at",
            "title",
            "upload_user__username",
            "upload_user__id",
        ).get(pk=article_id)
        article_info["content_html"] = article.get_content_html()
        

        return JsonResponse(article_info, safe=False)
