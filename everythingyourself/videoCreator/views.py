from mimetypes import guess_type
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .video  import render_video
from .forms import UploadFaceForm

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_video(request):
    if request.method == 'POST':
        form = UploadFaceForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['face']
            filename = 'face'
            tmp_path = 'faces/{}.png'.format(filename)
            path = default_storage.save(tmp_path, ContentFile(data.read()))

            id="2x3"
            videofile = render_video(id, fps=60)

            video_path = os.path.join(BASE_DIR, videofile)
            with open(video_path, 'rb') as f:
                response = HttpResponse(f, content_type='video/mp4')
                response['Content-Length'] = len(response.content)
                response['Content-Disposition'] = 'attachment; filename=export-2x3.mp4'
                return response

    uploadfaceform = UploadFaceForm()
    return render(request, 'videoCreator/create_video.html', {'UploadFaceForm': uploadfaceform})
