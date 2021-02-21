from django.shortcuts import render, redirect
from django.views import View
from .forms import ArticleUploadForm
from .models import Article
from django.core.files.storage import default_storage, FileSystemStorage
from django.conf import settings
#import ffmpeg

# Create your views here.
DATA_DIR = settings.MEDIA_ROOT


class HomeView(View):
    def get(self, request, *args, **kwargs):

        return render(request, "error_resolve_app/home.html")


class ArticleUploadView(View):
    def get(self, request, *args, **kwargs):

        context = {
            "form": ArticleUploadForm(),
        }

        return render(request, "error_resolve_app/upload.html", context)

    def post(self, request, *args, **kwargs):

        form = ArticleUploadForm(request.POST, request.FILES)

        if not form.is_valid():

            return render(
                request, "error_resolve_app/home.html", {"form": ArticleUploadForm()}
            )

        new_movie_name = form.cleaned_data["movie"].name
        new_article = Article()
        new_article.upload_file_name = new_movie_name
        new_article.save()

        try:
            storage = FileSystemStorage()
            storage.location = DATA_DIR + "/" + str(new_article.id)
            filename = storage.save(new_movie_name, form.cleaned_data["movie"])
            self.make_video_thumb(
                DATA_DIR + "/" + str(new_article.id) + "/" + filename,
                new_article.thumb_frame,
                DATA_DIR + "/" + str(new_article.id) + "/thumb.jpg",
            )

        except:
            self.delete_video(new_article.id, filename)
            new_article.delete()
            raise

        else:
            new_article.movie_name = filename
            new_article.save()

        return redirect("error_resolve_app:article_show", article_id=new_article.id)

    def make_video_thumb(self, src_filename, capture_frame, dst_filename=None):

        probe = ffmpeg.probe(src_filename)
        video_info = next(x for x in probe["streams"] if x["codec_type"] == "video")
        nframes = video_info["nb_frames"]
        avg_frame_rate = (lambda x: int(x[0]) / int(x[1]))(
            video_info["avg_frame_rate"].split("/")
        )
        start_position = int(capture_frame) / avg_frame_rate

        if dst_filename == None:
            out_target = "pipe:"
        else:
            out_target = dst_filename

        im = (
            ffmpeg.input(src_filename, ss=start_position)
            .filter("scale", 200, -1)
            .output(
                out_target,
                vframes=1,
                format="image2",
                vcodec="mjpeg",
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


class ArticleShow(View):
    def get(self, request, article_id, *args, **kwargs):

        article = Article.objects.get(pk=article_id)

        return render(
            request, "error_resolve_app/article_show.html", {"article": article}
        )
